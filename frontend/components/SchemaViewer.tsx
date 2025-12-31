'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Database, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api';

interface TableSchema {
  table_name: string;
  columns: Array<{
    name: string;
    type: string;
  }>;
}

export default function SchemaViewer() {
  const [schema, setSchema] = useState<TableSchema[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    try {
      const data = await apiClient.getSchema();
      setSchema(data.tables || []);
    } catch (error) {
      console.error('Failed to load schema:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Database className="h-5 w-5" />
          Database Schema
        </CardTitle>
        <CardDescription>
          Available tables and columns
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 overflow-auto">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : schema.length === 0 ? (
          <div className="text-center text-muted-foreground py-8">
            <p>No tables found</p>
          </div>
        ) : (
          <div className="space-y-4">
            {schema.map((table, index) => (
              <div
                key={index}
                className="border rounded-md p-4 space-y-2"
              >
                <h3 className="font-semibold text-sm">{table.table_name}</h3>
                <div className="space-y-1">
                  {table.columns.map((column, colIndex) => (
                    <div
                      key={colIndex}
                      className="flex items-center justify-between text-xs text-muted-foreground"
                    >
                      <span className="font-mono">{column.name}</span>
                      <span className="text-xs px-2 py-0.5 rounded bg-muted">
                        {column.type}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
