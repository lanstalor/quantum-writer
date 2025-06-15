'use client'

import { useState, useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useStory, useStoryChapters, useUpdateChapter } from '@/hooks/useStories'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ArrowLeft, Save } from 'lucide-react'
import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import Collaboration from '@tiptap/extension-collaboration'

interface EditPageProps {
  params: { id: string }
}

export default function EditPage({ params }: EditPageProps) {
  const router = useRouter()
  const { data: story, isLoading: storyLoading } = useStory(params.id)
  const { data: chapters, isLoading: chaptersLoading } = useStoryChapters(params.id)
  const updateChapter = useUpdateChapter()
  const [edited, setEdited] = useState<Record<string, string>>({})

  const WS_URL = process.env.NEXT_PUBLIC_WS_URL ?? 'ws://localhost:8000'

  function useCollab(chapterId: string) {
    const ydocRef = useRef<Y.Doc>()
    const providerRef = useRef<WebsocketProvider>()

    const editor = useEditor({
      extensions: [
        StarterKit,
        Collaboration.configure({ document: (ydocRef.current = new Y.Doc()) })
      ],
    })

    useEffect(() => {
      const provider = new WebsocketProvider(`${WS_URL}/ws/${chapterId}`, ydocRef.current!)
      providerRef.current = provider
      return () => {
        provider.destroy()
        ydocRef.current?.destroy()
      }
    }, [chapterId])

    return editor
  }

  function ChapterEditor({ chapter }: { chapter: any }) {
    const editor = useCollab(chapter.id)
    return (
      <Card key={chapter.id}>
        <CardHeader>
          <CardTitle>{chapter.title}</CardTitle>
          <CardDescription>Chapter {chapter.position}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {editor ? (
            <EditorContent editor={editor} className="border rounded p-2" />
          ) : (
            <Textarea
              value={edited[chapter.id] ?? chapter.content}
              onChange={(e) => setEdited({ ...edited, [chapter.id]: e.target.value })}
              rows={10}
            />
          )}
          <Button onClick={() => handleSave(chapter.id)} disabled={updateChapter.isPending}>
            <Save className="h-4 w-4 mr-2" /> Save
          </Button>
        </CardContent>
      </Card>
    )
  }

  const handleSave = async (chapterId: string) => {
    const content = edited[chapterId]
    if (content == null) return
    await updateChapter.mutateAsync({ id: chapterId, data: { content } })
  }

  if (storyLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-muted-foreground">Loading story...</p>
      </div>
    )
  }

  if (!story) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-red-500 mb-4">Story not found</p>
        <Link href="/stories">
          <Button>Back to Stories</Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8 space-y-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" onClick={() => router.push(`/stories/${params.id}`)}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Story
          </Button>
          <h1 className="text-2xl font-bold">Edit: {story.title}</h1>
        </div>
      </div>

      {chaptersLoading ? (
        <p className="text-muted-foreground">Loading chapters...</p>
      ) : chapters && chapters.length > 0 ? (
        <div className="space-y-6">
          {chapters.sort((a, b) => a.position - b.position).map(chapter => (
            <ChapterEditor key={chapter.id} chapter={chapter} />
          ))}
        </div>
      ) : (
        <p className="text-muted-foreground">No chapters available</p>
      )}
    </div>
  )
}

