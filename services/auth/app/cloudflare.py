import time
from typing import Any, Dict, Iterable

import httpx
from fastapi import HTTPException
from jose import jwk, jwt
from jose.exceptions import JWTError
from jose.utils import base64url_decode

from app.core import settings

_JWKS_CACHE: Dict[str, Any] | None = None
_JWKS_EXPIRES_AT: float = 0.0


async def _fetch_jwks() -> Dict[str, Any]:
    global _JWKS_CACHE, _JWKS_EXPIRES_AT
    if _JWKS_CACHE and time.time() < _JWKS_EXPIRES_AT:
        return _JWKS_CACHE
    if not settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN:
        raise HTTPException(status_code=503, detail="Cloudflare Access team domain not configured")
    url = f"https://{settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN}/cdn-cgi/access/certs"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
    _JWKS_CACHE = data
    _JWKS_EXPIRES_AT = time.time() + 3600
    return data


async def verify_access_token(token: str) -> Dict[str, Any]:
    if not settings.CLOUDFLARE_ACCESS_AUDIENCE or not settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN:
        raise HTTPException(status_code=503, detail="Cloudflare Access integration not configured")
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid Cloudflare Access token header") from exc

    jwks = await _fetch_jwks()
    keys = jwks.get("keys", [])
    matching = next((key for key in keys if key.get("kid") == header.get("kid")), None)
    if not matching:
        raise HTTPException(status_code=401, detail="Unknown Cloudflare Access signing key")

    public_key = jwk.construct(matching)
    message, encoded_signature = token.rsplit(".", 1)
    decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
    if not public_key.verify(message.encode("utf-8"), decoded_signature):
        raise HTTPException(status_code=401, detail="Cloudflare Access token signature verification failed")

    claims = jwt.get_unverified_claims(token)

    expected_audience = settings.CLOUDFLARE_ACCESS_AUDIENCE
    token_audience = claims.get("aud")
    if expected_audience:
        audiences: Iterable[str]
        if isinstance(token_audience, str):
            audiences = [token_audience]
        elif isinstance(token_audience, (list, tuple)):
            audiences = token_audience
        else:
            audiences = []
        if expected_audience not in audiences:
            raise HTTPException(status_code=401, detail="Cloudflare Access audience mismatch")

    issuer = claims.get("iss")
    expected_issuer = f"https://{settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN}"
    if issuer != expected_issuer:
        raise HTTPException(status_code=401, detail="Cloudflare Access issuer mismatch")

    expires_at = claims.get("exp")
    if isinstance(expires_at, (int, float)) and expires_at < time.time():
        raise HTTPException(status_code=401, detail="Cloudflare Access token expired")

    return claims
