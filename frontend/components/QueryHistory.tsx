'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { History, CheckCircle2, XCircle } from 'lucide-react';
import { apiClient } from '@/lib/api';

interface HistoryItem {
  id: number;
  natural_query: string;
  sql_query: string;
  success: boolean;
  timestamp: string;
}

interface QueryHistoryProps {
  onSelectQuery: (query: string) => void;
}

export default function QueryHistory({ onSelectQuery }: QueryHistoryProps) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await apiClient.getHistory(20);
      setHistory(data.history || []);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoading(false);
    }
  };

  // Refresh history every 10 seconds
  useEffect(() => {
    const interval = setInterval(loadHistory, 10000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <History className="h-5 w-5" />
          Query History
        </CardTitle>
        <CardDescription>
          Recent queries
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 overflow-auto">
        {loading ? (
          <div className="text-center text-muted-foreground py-8">
            <p>Loading...</p>
          </div>
        ) : history.length === 0 ? (
          <div className="text-center text-muted-foreground py-8">
            <p>No history yet</p>
          </div>
        ) : (
          <div className="space-y-2">
            {history.map((item) => (
              <button
                key={item.id}
                onClick={() => onSelectQuery(item.natural_query)}
                className="w-full text-left p-3 rounded-md border hover:bg-accent transition-colors"
              >
                <div className="flex items-start gap-2">
                  {item.success ? (
                    <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                  ) : (
                    <XCircle className="h-4 w-4 text-red-500 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      {item.natural_query}
                    </p>
                    <p className="text-xs text-muted-foreground font-mono truncate">
                      {item.sql_query}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
