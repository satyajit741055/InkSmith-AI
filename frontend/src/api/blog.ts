import client from './client';

export interface BlogGenerationRequest {
  prompt: string;
}

export interface BlogGenerationResponse {
  thread_id: string;
}

export interface BlogStatusResponse {
  thread_id: string;
  status: 'pending' | 'processing' | 'planning' | 'writing' | 'assembling' | 'completed' | 'failed';
  current_step: string | null;
  pdf_url: string | null;
  error_message: string | null;
}

export const blogAPI = {
  createBlog: (data: BlogGenerationRequest) =>
    client.post<BlogGenerationResponse>('/blog/', data),

  getBlogStatus: (threadId: string) =>
    client.get<BlogStatusResponse>(`/blog/${threadId}`),
};
