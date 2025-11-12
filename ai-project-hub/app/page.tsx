'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';

interface Project {
  id: string;
  title: string;
  type: 'doc' | 'prototype';
  path: string;
  lastModified: string;
}

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const response = await fetch('/api/projects');
      const data = await response.json();
      setProjects(data);
    } catch (error) {
      console.error('Error loading projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProjectContent = async (project: Project) => {
    setSelectedProject(project);
    setLoading(true);
    try {
      const response = await fetch(`/api/content?path=${encodeURIComponent(project.path)}&type=${project.type}`);
      const data = await response.json();
      setContent(data.content || '');
    } catch (error) {
      console.error('Error loading content:', error);
      setContent('Error loading content');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h1 className="text-xl font-bold text-gray-900 dark:text-white">AI Project Hub</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Docs & Prototypes</p>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4">
          {loading && projects.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400">Loading projects...</p>
          ) : projects.length === 0 ? (
            <p className="text-gray-500 dark:text-gray-400">No projects found</p>
          ) : (
            <div className="space-y-2">
              {projects.map((project) => (
                <button
                  key={project.id}
                  onClick={() => loadProjectContent(project)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    selectedProject?.id === project.id
                      ? 'bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100'
                      : 'bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-white'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{project.title}</span>
                    <span className={`text-xs px-2 py-1 rounded ${
                      project.type === 'doc' 
                        ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                        : 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200'
                    }`}>
                      {project.type === 'doc' ? 'Doc' : 'Code'}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {new Date(project.lastModified).toLocaleDateString()}
                  </p>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {selectedProject ? (
          <>
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">{selectedProject.title}</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {selectedProject.type === 'doc' ? 'Documentation' : 'Code Prototype'}
              </p>
            </div>
            <div className="flex-1 overflow-y-auto p-8">
              {loading ? (
                <p className="text-gray-500 dark:text-gray-400">Loading content...</p>
              ) : selectedProject.type === 'doc' ? (
                <div className="prose dark:prose-invert max-w-none">
                  <ReactMarkdown>{content}</ReactMarkdown>
                </div>
              ) : (
                <pre className="bg-gray-900 dark:bg-gray-950 text-gray-100 p-4 rounded-lg overflow-x-auto">
                  <code>{content}</code>
                </pre>
              )}
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Welcome to AI Project Hub</h2>
              <p className="text-gray-500 dark:text-gray-400">Select a project from the sidebar to view</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

