const API_BASE_URL = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1').replace(/\/$/, '');
console.log('NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL); // Debug log
console.log('API_BASE_URL:', API_BASE_URL); // Debug log

export interface ProcessingJob {
  id: number;
  document_id: number;
  status: 'queued' | 'processing' | 'completed' | 'failed';
  progress_percentage: number;
  current_stage: string;
  error_message?: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  extracted_title?: string;
  extracted_category?: string;
  extracted_summary?: string;
  extracted_keywords?: string[];
  processed_content?: string;
  final_result?: any;
  is_reviewed: boolean;
  is_finalized: boolean;
  celery_task_id?: string;
  document?: {
    id: number;
    filename: string;
    original_filename: string;
    file_type: string;
    file_size: number;
    upload_time: string;
  };
}

export interface ProgressEvent {
  job_id: number;
  status: string;
  progress_percentage: number;
  current_stage: string;
  message?: string;
  timestamp: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Document operations
  async uploadDocument(file: File): Promise<ProcessingJob> {
    const formData = new FormData();
    formData.append('file', file);

    const uploadUrl = `${this.baseUrl}/documents/upload`;
    console.log('Uploading to:', uploadUrl); // Debug log
    console.log('Base URL:', this.baseUrl); // Debug log

    const response = await fetch(uploadUrl, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  async getDocuments(skip = 0, limit = 100) {
    return this.request(`/documents?skip=${skip}&limit=${limit}`);
  }

  async deleteDocument(documentId: number) {
    return this.request(`/documents/${documentId}`, { method: 'DELETE' });
  }

  // Job operations
  async getJobs(params: {
    skip?: number;
    limit?: number;
    status?: string;
    search?: string;
    sort_by?: string;
    sort_order?: string;
  } = {}) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== '') {
        searchParams.append(key, value.toString());
      }
    });

    const queryString = searchParams.toString();
    return this.request(`/jobs${queryString ? `?${queryString}` : ''}`);
  }

  async getJob(jobId: number): Promise<ProcessingJob> {
    return this.request(`/jobs/${jobId}`);
  }

  async updateJob(jobId: number, data: Partial<ProcessingJob>): Promise<ProcessingJob> {
    return this.request(`/jobs/${jobId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async retryJob(jobId: number): Promise<ProcessingJob> {
    return this.request(`/jobs/${jobId}/retry`, { method: 'POST' });
  }

  async finalizeJob(jobId: number): Promise<{ message: string }> {
    return this.request(`/jobs/${jobId}/finalize`, { method: 'POST' });
  }

  async exportJobs(format: 'json' | 'csv', finalizedOnly = true): Promise<void> {
    const url = `${this.baseUrl}/jobs/export/${format}?finalized_only=${finalizedOnly}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`Export failed: ${response.status} ${response.statusText}`);
    }

    const blob = await response.blob();
    const downloadUrl = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = downloadUrl;
    a.download = `jobs_export.${format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(downloadUrl);
  }

  // WebSocket connection for progress tracking
  createProgressWebSocket(jobId: number): WebSocket {
    // Convert HTTP URL to WebSocket URL
    const wsBaseUrl = API_BASE_URL.replace(/^http/, 'ws');
    const wsUrl = `${wsBaseUrl}/ws/progress/${jobId}`;
    return new WebSocket(wsUrl);
  }
}

export const apiClient = new ApiClient();
