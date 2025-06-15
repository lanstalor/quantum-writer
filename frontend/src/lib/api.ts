export interface Story {
  id: string;
  user_id: string;
  title: string;
  genre?: string;
  description?: string;
  created_at: string;
  updated_at?: string;
  story_metadata?: Record<string, any>;
}

export interface CreateStoryRequest {
  title: string;
  genre?: string;
  description?: string;
  story_metadata?: Record<string, any>;
}

export interface Chapter {
  id: string;
  story_id: string;
  title: string;
  content: string;
  position: number;
  word_count: number;
  created_at: string;
  updated_at?: string;
}

export interface CreateChapterRequest {
  story_id: string;
  title: string;
  content: string;
  position?: number;
  branch_id?: string;
}

export interface GenerateChapterRequest {
  story_id: string;
  title: string;
  prompt: string;
  position?: number;
  system_prompt?: string;
}

export const queryKeys = {
  stories: ['stories'] as const,
  story: (id: string) => ['stories', id] as const,
  storyChapters: (id: string) => ['stories', id, 'chapters'] as const,
  chapter: (id: string) => ['chapters', id] as const,
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? '';
let token: string | null = null;
export function setToken(t: string | null) {
  token = t;
  if (typeof window !== 'undefined') {
    if (t) localStorage.setItem('token', t);
    else localStorage.removeItem('token');
  }
}

export function getToken() {
  return token;
}

export function isLoggedIn() {
  return !!token;
}

if (typeof window !== 'undefined') {
  const saved = localStorage.getItem('token');
  if (saved) token = saved;
}

async function request(path: string, options: RequestInit = {}) {
  const res = await fetch(`${API_URL}/api/v1${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function register(data: { username: string; password: string }) {
  const res = await fetch(`${API_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  setToken(json.access_token);
  return json;
}

export async function login(data: { username: string; password: string }) {
  const res = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  setToken(json.access_token);
  return json;
}

export const api = {
  getStories: () => request('/stories/'),
  getStory: (id: string) => request(`/stories/${id}`),
  createStory: (data: CreateStoryRequest) => request('/stories/', { method: 'POST', body: JSON.stringify(data) }),
  updateStory: (id: string, data: Partial<CreateStoryRequest>) => request(`/stories/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteStory: (id: string) => request(`/stories/${id}`, { method: 'DELETE' }),
  getStoryChapters: (storyId: string) => request(`/chapters/story/${storyId}`),
  getChapter: (id: string) => request(`/chapters/${id}`),
  createChapter: (data: CreateChapterRequest) => request('/chapters/', { method: 'POST', body: JSON.stringify(data) }),
  updateChapter: (id: string, data: Partial<CreateChapterRequest>) => request(`/chapters/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteChapter: (id: string) => request(`/chapters/${id}`, { method: 'DELETE' }),
  generateChapter: (data: GenerateChapterRequest) => request('/chapters/generate', { method: 'POST', body: JSON.stringify(data) }),
  reorderChapters: (storyId: string, positions: Record<string, number>) => request(`/chapters/story/${storyId}/reorder`, { method: 'PUT', body: JSON.stringify(positions) }),
};

