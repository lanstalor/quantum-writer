# Cloudflare Pages & Access Deployment Guide

This document captures the configuration required to publish the Quantum Writer frontend on Cloudflare Pages while delegating authentication to Cloudflare Access.

## 1. Prerequisites

1. A Cloudflare account with:
   - Access to Cloudflare Pages.
   - Cloudflare Access enabled for your account/zone.
2. A Pages project (e.g. `quantum-writer`) and `CLOUDFLARE_PAGES_PROJECT` repository variable containing the project slug.
3. API credentials stored as GitHub secrets:
   - `CLOUDFLARE_API_TOKEN` with `Pages:Edit` and `Pages:Deployments:Create` permissions.
   - `CLOUDFLARE_ACCOUNT_ID` for the target account.
4. A Cloudflare Access application protecting the Pages hostname with:
   - Audience tag (UUID) copied for the `CLOUDFLARE_ACCESS_AUDIENCE` variable.
   - Team domain (e.g. `my-team.cloudflareaccess.com`).
   - Optionally, an Access service token (Client ID/Secret) if you wish to call the Access identity API from other services.

## 2. Repository Configuration

### Environment variables

Create the following secrets/variables in your deployment environment:

| Name | Scope | Description |
| ---- | ----- | ----------- |
| `CLOUDFLARE_API_TOKEN` | GitHub Secret | API token with Pages permissions |
| `CLOUDFLARE_ACCOUNT_ID` | GitHub Secret | Account identifier |
| `CLOUDFLARE_PAGES_PROJECT` | GitHub Repository Variable | Cloudflare Pages project name |
| `AUTH_SERVICE_URL` | GitHub Variable/Secret | Public URL of the auth service exposed via your gateway |
| `NEXT_PUBLIC_API_URL` | GitHub Variable | Gateway URL (used in the browser) |
| `NEXT_PUBLIC_WS_URL` | GitHub Variable | WebSocket endpoint exposed publicly |
| `NEXT_PUBLIC_CLOUDFLARE_ACCESS_LOGIN` | GitHub Variable | Set to `true` to enable automatic Access login |
| `CLOUDFLARE_ACCESS_AUDIENCE` | GitHub Secret/Variable | Audience tag from the Access app |
| `CLOUDFLARE_ACCESS_TEAM_DOMAIN` | GitHub Variable | Team domain (`<team>.cloudflareaccess.com`) |
| `CLOUDFLARE_ACCESS_EMAIL_CLAIM` | Optional Variable | Override the email claim (defaults to `email`) |
| `CLOUDFLARE_ACCESS_ALLOWED_EMAILS` | Optional Variable | Comma separated allow-list for individual emails |
| `CLOUDFLARE_ACCESS_ALLOWED_DOMAINS` | Optional Variable | Comma separated allow-list for email domains |

Ensure the same Access-related variables are present in the runtime environment of the `auth` service (e.g. Kubernetes secret, Docker compose overrides).

### GitHub Actions Workflow

The repository contains `.github/workflows/deploy-cloudflare-pages.yml` which:

1. Builds the Next.js application with [`@cloudflare/next-on-pages`](https://github.com/cloudflare/next-on-pages).
2. Deploys the generated `.vercel/output` bundle to Cloudflare Pages.
3. Is automatically triggered on pushes to `main` or manually via *Run workflow*.

## 3. Cloudflare Access Integration Flow

1. User visits the Cloudflare Pages site and completes the Access challenge.
2. Access injects the `CF_Authorization` cookie/header with a signed JWT.
3. The frontend calls `/cloudflare/session`, a server-side route that:
   - Validates configuration.
   - Forwards the Access JWT to the auth service `/login/cloudflare` endpoint.
4. The auth service verifies the JWT signature against the Cloudflare JWKS, enforces allow-lists, auto-provisions a user, and returns Quantum Writer access/refresh tokens.
5. The frontend stores these tokens and continues calling the story services as normal.

## 4. Local Development Tips

- Leave `NEXT_PUBLIC_CLOUDFLARE_ACCESS_LOGIN` unset (default `false`) to use the built-in username/password login locally.
- When testing Access locally, export the relevant environment variables and send the `CF_Authorization` cookie via tools like `cloudflared access login`.
- The JWKS fetch is cached for one hour inside the auth service to avoid rate limits.

## 5. Troubleshooting

| Symptom | Likely Cause | Fix |
| ------- | ------------ | --- |
| `501 Cloudflare Access integration not configured` | Missing Access environment variables | Confirm variables on both frontend and auth service |
| `401 Missing Cloudflare Access token` | Request is not behind Access | Ensure the Pages domain is protected by Access |
| `403 Email not authorized` | Email/domain not on allow-list | Update `CLOUDFLARE_ACCESS_ALLOWED_*` variables |
| GitHub Action fails during build | `@cloudflare/next-on-pages` download blocked | Configure outbound network policy to allow npm registry access |

