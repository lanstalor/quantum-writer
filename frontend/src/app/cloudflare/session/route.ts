import { NextRequest, NextResponse } from 'next/server'

export const dynamic = 'force-dynamic'

function missingConfiguration() {
  return !process.env.CLOUDFLARE_ACCESS_TEAM_DOMAIN || !process.env.CLOUDFLARE_ACCESS_AUDIENCE
}

function resolveAuthServiceUrl() {
  return process.env.AUTH_SERVICE_URL || process.env.NEXT_PUBLIC_API_URL
}

export async function GET(request: NextRequest) {
  if (missingConfiguration()) {
    return NextResponse.json({ error: 'Cloudflare Access integration not configured' }, { status: 501 })
  }

  const token = request.cookies.get('CF_Authorization')?.value || request.headers.get('cf-authorization')
  if (!token) {
    return NextResponse.json({ error: 'Missing Cloudflare Access token' }, { status: 401 })
  }

  const authService = resolveAuthServiceUrl()
  if (!authService) {
    return NextResponse.json({ error: 'Auth service URL not configured' }, { status: 500 })
  }

  const endpoint = new URL('/login/cloudflare', authService)
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'CF-Authorization': token,
    },
    cache: 'no-store',
  })

  const text = await response.text()
  if (!response.ok) {
    try {
      const data = JSON.parse(text)
      return NextResponse.json(data, { status: response.status })
    } catch (error) {
      return NextResponse.json({ error: text || 'Unable to establish Cloudflare Access session' }, { status: response.status })
    }
  }

  return new NextResponse(text, {
    status: 200,
    headers: {
      'content-type': 'application/json',
    },
  })
}
