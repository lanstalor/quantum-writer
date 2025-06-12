import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BookOpen, Sparkles, Users, GitBranch } from 'lucide-react'
import Link from 'next/link'

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col">
      {/* Hero Section */}
      <section className="flex-1 flex items-center justify-center px-4 py-16">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold tracking-tighter mb-6">
            Quantum Writer
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            AI-assisted storytelling platform for creating complex narratives with advanced context management and collaborative features
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/stories">
              <Button size="lg">
                Get Started
              </Button>
            </Link>
            <Link href="/demo">
              <Button size="lg" variant="outline">
                View Demo
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline">
                Login
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-16 bg-muted/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <Sparkles className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>AI-Powered Writing</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Multiple AI models help you generate, continue, and refine your narrative
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <GitBranch className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>Branching Narratives</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Explore alternative storylines and merge the best elements
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <Users className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>Real-time Collaboration</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Work together with other writers in real-time with live updates
                </CardDescription>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <BookOpen className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>Smart Context</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription>
                  Advanced context management maintains narrative consistency
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </main>
  )
}
