'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getToken } from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useStories, useCreateStory } from '@/hooks/useStories';
import { BookOpen, Plus, Calendar, User } from 'lucide-react';
import Link from 'next/link';

const GENRES = [
  'fantasy',
  'science-fiction',
  'mystery',
  'romance',
  'thriller',
  'horror',
  'adventure',
  'historical-fiction',
  'literary-fiction',
  'young-adult',
  'other'
];

export default function StoriesPage() {
  const router = useRouter();
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newStory, setNewStory] = useState({
    title: '',
    genre: '',
    description: '',
  });

  const { data: stories, isLoading, error } = useStories();
  const createStoryMutation = useCreateStory();

  useEffect(() => {
    if (!getToken()) {
      router.push('/login');
    }
  }, [router]);

  const handleCreateStory = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newStory.title.trim()) return;

    try {
      await createStoryMutation.mutateAsync({
        title: newStory.title,
        genre: newStory.genre || undefined,
        description: newStory.description || undefined,
        story_metadata: {},
      });
      
      setNewStory({ title: '', genre: '', description: '' });
      setIsCreateDialogOpen(false);
    } catch (error) {
      console.error('Failed to create story:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Loading your stories...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <p className="text-red-500 mb-4">Failed to load stories</p>
            <p className="text-muted-foreground text-sm">{error.message}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">My Stories</h1>
          <p className="text-muted-foreground mt-1">
            {stories?.length || 0} {stories?.length === 1 ? 'story' : 'stories'}
          </p>
        </div>
        
        <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
          <DialogTrigger asChild>
            <Button size="lg">
              <Plus className="h-4 w-4 mr-2" />
              New Story
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>Create New Story</DialogTitle>
              <DialogDescription>
                Start a new AI-assisted story. You can always edit these details later.
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleCreateStory} className="space-y-4 mt-4">
              <div className="space-y-2">
                <Label htmlFor="title">Title *</Label>
                <Input
                  id="title"
                  placeholder="Enter your story title..."
                  value={newStory.title}
                  onChange={(e) => setNewStory({ ...newStory, title: e.target.value })}
                  required
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="genre">Genre</Label>
                <Select value={newStory.genre} onValueChange={(value) => setNewStory({ ...newStory, genre: value })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a genre..." />
                  </SelectTrigger>
                  <SelectContent>
                    {GENRES.map((genre) => (
                      <SelectItem key={genre} value={genre}>
                        {genre.charAt(0).toUpperCase() + genre.slice(1).replace('-', ' ')}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  placeholder="Brief description of your story..."
                  value={newStory.description}
                  onChange={(e) => setNewStory({ ...newStory, description: e.target.value })}
                  rows={3}
                />
              </div>
              
              <div className="flex justify-end space-x-2 pt-4">
                <Button type="button" variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={createStoryMutation.isPending || !newStory.title.trim()}>
                  {createStoryMutation.isPending ? 'Creating...' : 'Create Story'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Stories Grid */}
      {stories && stories.length > 0 ? (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {stories.map((story) => (
            <Link key={story.id} href={`/stories/${story.id}`}>
              <Card className="h-full hover:shadow-md transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <BookOpen className="h-8 w-8 text-primary mb-2" />
                    {story.genre && (
                      <span className="text-xs bg-secondary text-secondary-foreground px-2 py-1 rounded-full">
                        {story.genre.charAt(0).toUpperCase() + story.genre.slice(1).replace('-', ' ')}
                      </span>
                    )}
                  </div>
                  <CardTitle className="line-clamp-2">{story.title}</CardTitle>
                  {story.description && (
                    <CardDescription className="line-clamp-3">
                      {story.description}
                    </CardDescription>
                  )}
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      {new Date(story.created_at).toLocaleDateString()}
                    </div>
                    <div className="flex items-center">
                      <User className="h-4 w-4 mr-1" />
                      {story.user_id.substring(0, 8)}...
                    </div>
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      ) : (
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center max-w-md">
            <BookOpen className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">No stories yet</h3>
            <p className="text-muted-foreground mb-6">
              Start your first AI-assisted story by clicking the button below.
            </p>
            <Button onClick={() => setIsCreateDialogOpen(true)} size="lg">
              <Plus className="h-4 w-4 mr-2" />
              Create Your First Story
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}