// React Query hooks for story management

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api, queryKeys, Story, CreateStoryRequest, Chapter, CreateChapterRequest, GenerateChapterRequest } from '@/lib/api';

// Story hooks
export function useStories() {
  return useQuery({
    queryKey: queryKeys.stories,
    queryFn: () => api.getStories(),
  });
}

export function useStory(id: string) {
  return useQuery({
    queryKey: queryKeys.story(id),
    queryFn: () => api.getStory(id),
    enabled: !!id,
  });
}

export function useCreateStory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateStoryRequest) => api.createStory(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.stories });
    },
  });
}

export function useUpdateStory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateStoryRequest> }) =>
      api.updateStory(id, data),
    onSuccess: (story) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.stories });
      queryClient.setQueryData(queryKeys.story(story.id), story);
    },
  });
}

export function useDeleteStory() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.deleteStory(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.stories });
    },
  });
}

// Chapter hooks
export function useStoryChapters(storyId: string) {
  return useQuery({
    queryKey: queryKeys.storyChapters(storyId),
    queryFn: () => api.getStoryChapters(storyId),
    enabled: !!storyId,
  });
}

export function useChapter(id: string) {
  return useQuery({
    queryKey: queryKeys.chapter(id),
    queryFn: () => api.getChapter(id),
    enabled: !!id,
  });
}

export function useCreateChapter() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateChapterRequest) => api.createChapter(data),
    onSuccess: (chapter) => {
      queryClient.invalidateQueries({ 
        queryKey: queryKeys.storyChapters(chapter.story_id) 
      });
    },
  });
}

export function useUpdateChapter() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<CreateChapterRequest> }) =>
      api.updateChapter(id, data),
    onSuccess: (chapter) => {
      queryClient.invalidateQueries({ 
        queryKey: queryKeys.storyChapters(chapter.story_id) 
      });
      queryClient.setQueryData(queryKeys.chapter(chapter.id), chapter);
    },
  });
}

export function useDeleteChapter() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => api.deleteChapter(id),
    onSuccess: () => {
      // Note: We'd need the storyId to invalidate properly
      // For now, invalidate all stories queries
      queryClient.invalidateQueries({ queryKey: queryKeys.stories });
    },
  });
}

// AI Generation hook
export function useGenerateChapter() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: GenerateChapterRequest) => api.generateChapter(data),
    onSuccess: (chapter) => {
      queryClient.invalidateQueries({ 
        queryKey: queryKeys.storyChapters(chapter.story_id) 
      });
    },
  });
}

// Reorder chapters hook
export function useReorderChapters() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ storyId, positions }: { storyId: string; positions: Record<string, number> }) =>
      api.reorderChapters(storyId, positions),
    onSuccess: (_, { storyId }) => {
      queryClient.invalidateQueries({ 
        queryKey: queryKeys.storyChapters(storyId) 
      });
    },
  });
}

export function useStoryBranches(storyId: string) {
  return useQuery({
    queryKey: queryKeys.storyBranches(storyId),
    queryFn: () => api.getStoryBranches(storyId),
    enabled: !!storyId,
  });
}

export function useMergeBranch() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ storyId, branchId }: { storyId: string; branchId: string }) =>
      api.mergeBranch(branchId),
    onSuccess: (_, { storyId }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.storyBranches(storyId) });
      queryClient.invalidateQueries({ queryKey: queryKeys.storyChapters(storyId) });
    },
  });
}