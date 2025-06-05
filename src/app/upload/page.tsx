'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation } from '@tanstack/react-query';
import { ArrowUpTrayIcon, DocumentTextIcon } from '@heroicons/react/24/outline';

export default function UploadPage() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch('http://localhost:8000/api/v1/resumes/upload', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error('Failed to upload resume');
      return res.json();
    },
  });

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      uploadMutation.mutate(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': [
        '.docx',
      ],
    },
    maxFiles: 1,
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Upload Resume</h1>
        <p className="mt-2 text-gray-600">
          Upload a resume for analysis and bias detection
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 text-center ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 hover:border-indigo-500'
        }`}
      >
        <input {...getInputProps()} />
        <ArrowUpTrayIcon className="h-12 w-12 text-gray-400" />
        <p className="mt-4 text-sm font-medium text-gray-900">
          {isDragActive
            ? 'Drop the resume here'
            : 'Drag and drop your resume, or click to browse'}
        </p>
        <p className="mt-1 text-xs text-gray-500">
          PDF, DOC, DOCX or TXT files up to 10MB
        </p>
      </div>

      {uploadedFile && (
        <div className="rounded-lg bg-white p-6 shadow">
          <div className="flex items-center space-x-3">
            <DocumentTextIcon className="h-10 w-10 text-indigo-500" />
            <div>
              <h3 className="text-sm font-medium text-gray-900">
                {uploadedFile.name}
              </h3>
              <p className="text-sm text-gray-500">
                {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
        </div>
      )}

      {uploadMutation.isPending && (
        <div className="rounded-lg bg-white p-6 shadow">
          <div className="flex items-center justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
            <span className="ml-3 text-sm font-medium text-gray-900">
              Analyzing resume...
            </span>
          </div>
        </div>
      )}

      {uploadMutation.isSuccess && (
        <div className="rounded-lg bg-white p-6 shadow">
          <h2 className="text-lg font-medium text-gray-900">Analysis Results</h2>
          <div className="mt-4 space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Decision</h3>
              <p className="mt-1 text-lg font-semibold text-gray-900">
                {uploadMutation.data.decision}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">
                Confidence Score
              </h3>
              <p className="mt-1 text-lg font-semibold text-gray-900">
                {(uploadMutation.data.confidence * 100).toFixed(1)}%
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Bias Metrics</h3>
              <dl className="mt-2 grid grid-cols-1 gap-4 sm:grid-cols-3">
                <div>
                  <dt className="text-xs text-gray-500">Demographic Parity</dt>
                  <dd className="text-sm font-medium text-gray-900">
                    {uploadMutation.data.bias_metrics.demographic_parity.toFixed(2)}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Equal Opportunity</dt>
                  <dd className="text-sm font-medium text-gray-900">
                    {uploadMutation.data.bias_metrics.equal_opportunity.toFixed(2)}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Disparate Impact</dt>
                  <dd className="text-sm font-medium text-gray-900">
                    {uploadMutation.data.bias_metrics.disparate_impact.toFixed(2)}
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      )}

      {uploadMutation.isError && (
        <div className="rounded-lg bg-red-50 p-6">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">
                Failed to upload resume
              </h3>
              <p className="mt-1 text-sm text-red-700">
                {uploadMutation.error instanceof Error
                  ? uploadMutation.error.message
                  : 'An error occurred'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 