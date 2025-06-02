'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useStory, useStoryChapters, useGenerateChapter } from '@/hooks/useStories';
import { ArrowLeft, Plus, BookOpen, Sparkles, Edit, Calendar } from 'lucide-react';
import Link from 'next/link';

interface StoryPageProps {
  params: {
    id: string;
  };
}

export default function StoryPage({ params }: StoryPageProps) {
  const router = useRouter();
  const [isGenerateDialogOpen, setIsGenerateDialogOpen] = useState(false);
  const [isReadDialogOpen, setIsReadDialogOpen] = useState(false);
  const [selectedChapter, setSelectedChapter] = useState<any>(null);
  const [newChapter, setNewChapter] = useState({
    title: '',
    prompt: '',
    system_prompt: '',
  });

  const { data: story, isLoading: storyLoading, error: storyError } = useStory(params.id);
  const { data: chapters, isLoading: chaptersLoading } = useStoryChapters(params.id);
  const generateChapterMutation = useGenerateChapter();

  const handleGenerateChapter = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newChapter.title.trim() || !newChapter.prompt.trim()) return;

    try {
      await generateChapterMutation.mutateAsync({
        story_id: params.id,
        title: newChapter.title,
        prompt: newChapter.prompt,
        system_prompt: newChapter.system_prompt || undefined,
        position: (chapters?.length || 0) + 1,
      });
      
      setNewChapter({ title: '', prompt: '', system_prompt: '' });
      setIsGenerateDialogOpen(false);
    } catch (error) {
      console.error('Failed to generate chapter:', error);
    }
  };

  if (storyLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Loading story...</p>
          </div>
        </div>
      </div>
    );
  }

  if (storyError || !story) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <p className="text-red-500 mb-4">Story not found</p>
            <Link href="/stories">
              <Button>Back to Stories</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-4">
          <Link href="/stories">
            <Button variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Stories
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold">{story.title}</h1>
            <div className="flex items-center space-x-4 mt-2 text-sm text-muted-foreground">
              {story.genre && (
                <span className="bg-secondary text-secondary-foreground px-2 py-1 rounded-full">
                  {story.genre.charAt(0).toUpperCase() + story.genre.slice(1).replace('-', ' ')}
                </span>
              )}
              <div className="flex items-center">
                <Calendar className="h-4 w-4 mr-1" />
                {new Date(story.created_at).toLocaleDateString()}
              </div>
              <span>{chapters?.length || 0} chapters</span>
            </div>
            {story.description && (
              <p className="text-muted-foreground mt-2">{story.description}</p>
            )}
          </div>
        </div>
        
        <Dialog open={isGenerateDialogOpen} onOpenChange={setIsGenerateDialogOpen}>
          <DialogTrigger asChild>
            <Button size="lg">
              <Sparkles className="h-4 w-4 mr-2" />
              Generate Chapter
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>Generate New Chapter with AI</DialogTitle>
              <DialogDescription>
                Describe what you want to happen in this chapter and let AI write it for you.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleGenerateChapter} className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label htmlFor="chapter-title">Chapter Title *</Label>
                <Input
                  id="chapter-title"
                  placeholder="e.g., Chapter 1: The Discovery"
                  value={newChapter.title}
                  onChange={(e) => setNewChapter({ ...newChapter, title: e.target.value })}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="chapter-prompt">What should happen in this chapter? *</Label>
                <Textarea
                  id="chapter-prompt"
                  placeholder="Describe the events, character interactions, plot developments, or scenes you want in this chapter..."
                  value={newChapter.prompt}
                  onChange={(e) => setNewChapter({ ...newChapter, prompt: e.target.value })}
                  rows={4}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="system-prompt">Writing Style Instructions (Optional)</Label>
                <Textarea
                  id="system-prompt"
                  placeholder="e.g., Write in Pierce Brown's visceral style with short punchy sentences..."
                  value={newChapter.system_prompt}
                  onChange={(e) => setNewChapter({ ...newChapter, system_prompt: e.target.value })}
                  rows={2}
                />
              </div>
              
              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsGenerateDialogOpen(false)}>
                  Cancel
                </Button>
                <Button 
                  type="submit" 
                  disabled={generateChapterMutation.isPending || !newChapter.title.trim() || !newChapter.prompt.trim()}
                >
                  {generateChapterMutation.isPending ? 'Generating...' : 'Generate Chapter'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Chapters List */}
      {chaptersLoading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      ) : chapters && chapters.length > 0 ? (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">Chapters</h2>
          {chapters
            .sort((a, b) => a.position - b.position)
            .map((chapter) => (
              <Card key={chapter.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div>
                      <CardTitle className="flex items-center">
                        <BookOpen className="h-5 w-5 mr-2 text-primary" />
                        {chapter.title}
                      </CardTitle>
                      <CardDescription className="flex items-center space-x-4 mt-1">
                        <span>Position: {chapter.position}</span>
                        <span>Words: {chapter.word_count}</span>
                        <span>Version: {chapter.version}</span>
                      </CardDescription>
                    </div>
                    <Button variant="ghost" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm max-w-none">
                    <p className="text-muted-foreground line-clamp-3">
                      {chapter.content ? chapter.content.substring(0, 200) + '...' : 'No content available'}
                    </p>
                  </div>
                  <div className="mt-4">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={() => {
                        setSelectedChapter(chapter);
                        setIsReadDialogOpen(true);
                      }}
                    >
                      Read Full Chapter
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
        </div>
      ) : (
        <div className="flex items-center justify-center py-20">
          <div className="text-center max-w-md">
            <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">No chapters yet</h3>
            <p className="text-muted-foreground mb-6">
              Start writing your story by generating the first chapter with AI assistance.
            </p>
            <Button onClick={() => setIsGenerateDialogOpen(true)} size="lg">
              <Sparkles className="h-4 w-4 mr-2" />
              Generate First Chapter
            </Button>
          </div>
        </div>
      )}

      {/* Read Chapter Dialog */}
      <Dialog open={isReadDialogOpen} onOpenChange={setIsReadDialogOpen}>
        <DialogContent className="max-w-4xl h-[85vh] flex flex-col">
          <DialogHeader className="flex-shrink-0">
            <DialogTitle>{selectedChapter?.title}</DialogTitle>
            <DialogDescription>
              Chapter {selectedChapter?.position} • {selectedChapter?.word_count} words
            </DialogDescription>
          </DialogHeader>
          <div className="flex-1 overflow-y-auto mt-4 pr-2">
            <div className="prose prose-sm max-w-none">
              <div className="whitespace-pre-wrap text-base leading-relaxed">
                {selectedChapter?.content ? 
                  selectedChapter.content
                    .replace(/^.*?(\*\*Chapter.*?\*\*)/s, '$1') // Remove content before first chapter marker
                    .replace(/---[\s\S]*?---/g, '') // Remove --- sections
                    .replace(/\*\*Perspective change:\*\*[\s\S]*?---/g, '') // Remove perspective change sections
                    .replace(/^\s+|\s+$/g, '') // Trim whitespace
                  : 'No content available'
                }
              </div>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}