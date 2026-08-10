import client from './client';

export interface BlogGenerationRequest {
  prompt: string;
}

export interface BlogGenerationResponse {
  thread_id: string;
}

export interface BlogStatusResponse {
  thread_id: string;
  status: 'pending' | 'processing' | 'routing' | 'researching' | 'planning' | 'writing' | 'merging' | 'image_planning' | 'generating_images' | 'completed' | 'failed';
  current_step: string | null;
  pdf_url: string | null;
  file_name: string | null;
  error_message: string | null;
}

export const blogAPI = {
  createBlog: (data: BlogGenerationRequest) =>
    client.post<BlogGenerationResponse>('/blog/', data),

  getBlogStatus: (threadId: string) =>
    client.get<BlogStatusResponse>(`/blog/${threadId}`),

  listBlogs: () =>
    client.get<BlogStatusResponse[]>('/blog/list'),

  downloadPdf: (threadId: string) =>
    client.get(`/blog/${threadId}/pdf`, { responseType: 'blob' }),
};
