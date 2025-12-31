'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import QueryInput from '@/components/QueryInput';
import QueryOutput from '@/components/QueryOutput';
import SchemaViewer from '@/components/SchemaViewer';
import QueryHistory from '@/components/QueryHistory';
import { apiClient } from '@/lib/api';

interface QueryResult {
  success: boolean;
  sql_query?: string;
  results?: any[];
  columns?: string[];
  row_count?: number;
  execution_time?: number;
  error?: string;
}

export default function Home() {
  const [result, setResult] = useState<QueryResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');

  const handleQuerySubmit = async (query: string) => {
    setIsLoading(true);
    setCurrentQuery(query);
    
    try {
      const data = await apiClient.executeQuery(query);
      setResult(data);
    } catch (error) {
      console.error('Query execution failed:', error);
      setResult({
        success: false,
        error: error instanceof Error ? error.message : 'Failed to execute query',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleHistorySelect = (query: string) => {
    setCurrentQuery(query);
    // Optionally auto-execute
    // handleQuerySubmit(query);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
          {/* Left Sidebar - Schema & History */}
          <div className="col-span-12 lg:col-span-3 space-y-4 overflow-auto">
            <div className="h-[45%]">
              <SchemaViewer />
            </div>
            <div className="h-[50%]">
              <QueryHistory onSelectQuery={handleHistorySelect} />
            </div>
          </div>

          {/* Main Content - Split Screen */}
          <div className="col-span-12 lg:col-span-9">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
              {/* Left Panel - Input */}
              <div className="h-full">
                <QueryInput onSubmit={handleQuerySubmit} isLoading={isLoading} />
              </div>

              {/* Right Panel - Output */}
              <div className="h-full">
                <QueryOutput result={result} />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
