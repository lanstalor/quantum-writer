'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { login } from '@/lib/api'

export default function LoginPage() {
  const router = useRouter()
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await login(form)
      router.push('/stories')
    } catch (err: any) {
      setError('Failed to login')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen p-4">
      <form onSubmit={handleSubmit} className="space-y-4 w-full max-w-sm">
        <div className="space-y-2">
          <Label htmlFor="username">Username</Label>
          <Input id="username" value={form.username} onChange={e => setForm({ ...form, username: e.target.value })} required />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input type="password" id="password" value={form.password} onChange={e => setForm({ ...form, password: e.target.value })} required />
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <Button type="submit" className="w-full">Login</Button>
      </form>
    </div>
  )
}

