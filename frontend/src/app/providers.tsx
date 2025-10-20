'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ThemeProvider } from 'next-themes'
import { useMemo, useState } from 'react'

import { useCloudflareAccessLogin } from '@/hooks/useCloudflareAccessLogin'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
          },
        },
      })
  )
  const accessEnabled = useMemo(() => process.env.NEXT_PUBLIC_CLOUDFLARE_ACCESS_LOGIN === 'true', [])
  useCloudflareAccessLogin(accessEnabled)

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        {children}
      </ThemeProvider>
    </QueryClientProvider>
  )
}