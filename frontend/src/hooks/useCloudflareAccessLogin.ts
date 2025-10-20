'use client'

import { useCallback, useEffect, useState } from 'react'

import { getToken, setRefreshToken, setToken } from '@/lib/api'

type Status = 'idle' | 'loading' | 'success' | 'error'

async function establishSession() {
  const response = await fetch('/cloudflare/session', {
    method: 'GET',
    credentials: 'include',
  })
  if (!response.ok) {
    throw new Error(await response.text())
  }
  return response.json()
}

export function useCloudflareAccessLogin(enabled: boolean) {
  const [status, setStatus] = useState<Status>('idle')
  const [error, setError] = useState<string | null>(null)

  const synchronize = useCallback(async () => {
    if (!enabled || typeof window === 'undefined') {
      return
    }
    if (getToken()) {
      return
    }
    setStatus('loading')
    setError(null)
    try {
      const session = await establishSession()
      if (session?.access_token) {
        setToken(session.access_token)
      }
      if (session?.refresh_token) {
        setRefreshToken(session.refresh_token)
      }
      setStatus('success')
    } catch (err) {
      setStatus('error')
      setError(err instanceof Error ? err.message : 'Unable to establish Cloudflare Access session')
    }
  }, [enabled])

  useEffect(() => {
    synchronize()
  }, [synchronize])

  return { status, error }
}
