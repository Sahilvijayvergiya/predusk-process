'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiClient, ProcessingJob, ProgressEvent } from '@/lib/api';
import { 
  ArrowLeft, 
  Edit3, 
  Save, 
  X, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  RotateCcw,
  Download,
  FileText,
  Tag
} from 'lucide-react';

interface JobDetailProps {
  jobId: number;
  onBack: () => void;
}

export default function JobDetail({ jobId, onBack }: JobDetailProps) {
  const [job, setJob] = useState<ProcessingJob | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState<Partial<ProcessingJob>>({});
  const [ws, setWs] = useState<WebSocket | null>(null);

  const fetchJob = useCallback(async () => {
    try {
      const jobData = await apiClient.getJob(jobId);
      setJob(jobData);
      setEditForm({
        extracted_title: jobData.extracted_title,
        extracted_category: jobData.extracted_category,
        extracted_summary: jobData.extracted_summary,
        extracted_keywords: jobData.extracted_keywords,
      });
    } catch (error) {
      console.error('Failed to fetch job:', error);
    } finally {
      setLoading(false);
    }
  }, [jobId]);

  useEffect(() => {
    fetchJob();
  }, [fetchJob]);

  useEffect(() => {
    // Set up WebSocket for real-time progress updates
    if (job && (job.status === 'queued' || job.status === 'processing')) {
      const websocket = apiClient.createProgressWebSocket(jobId);
      
      websocket.onopen = () => {
        console.log('WebSocket connected for job progress');
      };

      websocket.onmessage = (event) => {
        try {
          const progressEvent: ProgressEvent = JSON.parse(event.data);
          
          // Update job with progress information
          setJob(prev => prev ? {
            ...prev,
            status: progressEvent.status as any,
            progress_percentage: progressEvent.progress_percentage,
            current_stage: progressEvent.current_stage,
          } : null);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      websocket.onclose = () => {
        console.log('WebSocket disconnected');
      };

      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      setWs(websocket);

      return () => {
        websocket.close();
      };
    }
  }, [jobId, job?.status]);

  const handleSave = async () => {
    if (!job) return;

    try {
      const updatedJob = await apiClient.updateJob(jobId, editForm);
      setJob(updatedJob);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update job:', error);
    }
  };

  const handleRetry = async () => {
    if (!job) return;

    try {
      await apiClient.retryJob(jobId);
      fetchJob(); // Refresh job data
    } catch (error) {
      console.error('Failed to retry job:', error);
    }
  };

  const handleFinalize = async () => {
    if (!job) return;

    try {
      await apiClient.finalizeJob(jobId);
      fetchJob(); // Refresh job data
    } catch (error) {
      console.error('Failed to finalize job:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'processing':
        return <Clock className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!job) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Job not found</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md">
        <div className="p-6">
          {/* Header */}
          <div className="flex justify-between items-start mb-6">
            <div className="flex items-center">
              <button
                onClick={onBack}
                className="mr-4 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              >
                <ArrowLeft className="h-5 w-5" />
              </button>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                  <FileText className="mr-2" />
                  {job.document?.original_filename || 'Unknown Document'}
                </h2>
                <p className="text-gray-600 mt-1">Job ID: {job.id}</p>
              </div>
            </div>
            
            <div className="flex space-x-2">
              {job.status === 'completed' && !job.is_finalized && (
                <button
                  onClick={handleFinalize}
                  className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                >
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Finalize
                </button>
              )}
              
              {job.status === 'failed' && (
                <button
                  onClick={handleRetry}
                  className="flex items-center px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors"
                >
                  <RotateCcw className="h-4 w-4 mr-2" />
                  Retry
                </button>
              )}
              
              {job.status === 'completed' && !isEditing && (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
                >
                  <Edit3 className="h-4 w-4 mr-2" />
                  Edit
                </button>
              )}
              
              {isEditing && (
                <div className="flex space-x-2">
                  <button
                    onClick={handleSave}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
                  >
                    <Save className="h-4 w-4 mr-2" />
                    Save
                  </button>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setEditForm({
                        extracted_title: job.extracted_title,
                        extracted_category: job.extracted_category,
                        extracted_summary: job.extracted_summary,
                        extracted_keywords: job.extracted_keywords,
                      });
                    }}
                    className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors"
                  >
                    <X className="h-4 w-4 mr-2" />
                    Cancel
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Status and Progress */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Status</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  {getStatusIcon(job.status)}
                  <span className={`ml-2 px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(job.status)}`}>
                    {job.status}
                  </span>
                  {job.is_finalized && (
                    <span className="ml-2 px-3 py-1 text-sm font-medium rounded-full bg-purple-100 text-purple-800">
                      Finalized
                    </span>
                  )}
                </div>
                
                <div>
                  <div className="flex justify-between text-sm text-gray-600 mb-1">
                    <span>Progress</span>
                    <span>{Math.round(job.progress_percentage)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${job.progress_percentage}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">{job.current_stage}</p>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Timeline</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Created:</span>
                  <span className="text-gray-900">{formatDate(job.created_at)}</span>
                </div>
                {job.started_at && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Started:</span>
                    <span className="text-gray-900">{formatDate(job.started_at)}</span>
                  </div>
                )}
                {job.completed_at && (
                  <div className="flex justify-between">
                    <span className="text-gray-600">Completed:</span>
                    <span className="text-gray-900">{formatDate(job.completed_at)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Extracted Information */}
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Extracted Information</h3>
              
              <div className="space-y-4">
                {/* Title */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.extracted_title || ''}
                      onChange={(e) => setEditForm(prev => ({ ...prev, extracted_title: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="text-gray-900">{job.extracted_title || 'Not extracted'}</p>
                  )}
                </div>

                {/* Category */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.extracted_category || ''}
                      onChange={(e) => setEditForm(prev => ({ ...prev, extracted_category: e.target.value }))}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="text-gray-900">{job.extracted_category || 'Not extracted'}</p>
                  )}
                </div>

                {/* Summary */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Summary</label>
                  {isEditing ? (
                    <textarea
                      value={editForm.extracted_summary || ''}
                      onChange={(e) => setEditForm(prev => ({ ...prev, extracted_summary: e.target.value }))}
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <p className="text-gray-900">{job.extracted_summary || 'Not extracted'}</p>
                  )}
                </div>

                {/* Keywords */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Keywords</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={editForm.extracted_keywords?.join(', ') || ''}
                      onChange={(e) => setEditForm(prev => ({ 
                        ...prev, 
                        extracted_keywords: e.target.value.split(',').map(k => k.trim()).filter(k => k)
                      }))}
                      placeholder="Enter keywords separated by commas"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  ) : (
                    <div className="flex flex-wrap gap-2">
                      {job.extracted_keywords?.map((keyword, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800"
                        >
                          <Tag className="h-3 w-3 mr-1" />
                          {keyword}
                        </span>
                      )) || <span className="text-gray-500">No keywords extracted</span>}
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Error Message */}
            {job.error_message && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Error Details</h3>
                <div className="bg-red-50 border border-red-200 rounded-md p-4">
                  <p className="text-red-800">{job.error_message}</p>
                </div>
              </div>
            )}

            {/* Processed Content */}
            {job.processed_content && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Processed Content</h3>
                <div className="bg-gray-50 rounded-md p-4 max-h-64 overflow-y-auto">
                  <pre className="text-sm text-gray-700 whitespace-pre-wrap">{job.processed_content}</pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
