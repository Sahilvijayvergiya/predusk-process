'use client';

import { useState } from 'react';
import DocumentUpload from '@/components/DocumentUpload';
import JobsDashboard from '@/components/JobsDashboard';
import JobDetail from '@/components/JobDetail';
import { ProcessingJob } from '@/lib/api';

export default function Home() {
  const [currentView, setCurrentView] = useState<'upload' | 'dashboard' | 'detail'>('upload');
  const [selectedJob, setSelectedJob] = useState<ProcessingJob | null>(null);

  const handleUploadComplete = (job: ProcessingJob) => {
    alert(`Document "${job.document?.original_filename}" uploaded successfully!`);
    setCurrentView('dashboard');
  };

  const handleError = (error: string) => {
    alert(error);
  };

  const handleJobSelect = (job: ProcessingJob) => {
    setSelectedJob(job);
    setCurrentView('detail');
  };

  const handleBackToDashboard = () => {
    setSelectedJob(null);
    setCurrentView('dashboard');
  };

  const handleBackToUpload = () => {
    setSelectedJob(null);
    setCurrentView('upload');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                Document Processing System
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={handleBackToUpload}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'upload'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Upload
              </button>
              <button
                onClick={handleBackToDashboard}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  currentView === 'dashboard'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="py-8">
        {currentView === 'upload' && (
          <DocumentUpload
            onUploadComplete={handleUploadComplete}
            onError={handleError}
          />
        )}
        
        {currentView === 'dashboard' && (
          <JobsDashboard onJobSelect={handleJobSelect} />
        )}
        
        {currentView === 'detail' && selectedJob && (
          <JobDetail
            jobId={selectedJob.id}
            onBack={handleBackToDashboard}
          />
        )}
      </main>
    </div>
  );
}
