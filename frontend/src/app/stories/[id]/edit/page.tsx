'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useStory, useStoryChapters, useUpdateChapter, useStoryBranches, useMergeBranch } from '@/hooks/useStories'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { ArrowLeft, Save } from 'lucide-react'

interface EditPageProps {
  params: { id: string }
}

export default function EditPage({ params }: EditPageProps) {
  const router = useRouter()
  const { data: story, isLoading: storyLoading } = useStory(params.id)
  const { data: chapters, isLoading: chaptersLoading } = useStoryChapters(params.id)
  const { data: branches, isLoading: branchesLoading } = useStoryBranches(params.id)
  const mergeBranch = useMergeBranch()
  const updateChapter = useUpdateChapter()
  const [edited, setEdited] = useState<Record<string, string>>({})

  const handleMerge = async (branchId: string) => {
    await mergeBranch.mutateAsync({ storyId: params.id, branchId })
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

      {branchesLoading ? (
        <p className="text-muted-foreground">Loading branches...</p>
      ) : branches && branches.length > 0 ? (
        <div className="space-y-2">
          <h2 className="text-lg font-semibold">Branches</h2>
          <ul className="space-y-1">
            {branches.map(b => (
              <li key={b.id} className="flex items-center justify-between">
                <span>
                  {b.name} {b.status === 'merged' ? '(merged)' : ''}
                </span>
                {b.parent_branch_id && b.status === 'active' && (
                  <Button size="sm" onClick={() => handleMerge(b.id)}>Merge</Button>
                )}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {chaptersLoading ? (
        <p className="text-muted-foreground">Loading chapters...</p>
      ) : chapters && chapters.length > 0 ? (
        <div className="space-y-6">
          {chapters.sort((a, b) => a.position - b.position).map(chapter => (
            <Card key={chapter.id}>
              <CardHeader>
                <CardTitle>{chapter.title}</CardTitle>
                <CardDescription>Chapter {chapter.position}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  value={edited[chapter.id] ?? chapter.content}
                  onChange={e => setEdited({ ...edited, [chapter.id]: e.target.value })}
                  rows={10}
                />
                <Button
                  onClick={() => handleSave(chapter.id)}
                  disabled={updateChapter.isPending}
                >
                  <Save className="h-4 w-4 mr-2" /> Save
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <p className="text-muted-foreground">No chapters available</p>
      )}
    </div>
  )
}

