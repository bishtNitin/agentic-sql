'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { CheckCircle2, XCircle, Clock, Database, Copy, Check } from 'lucide-react';
import { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from './ui/button';

interface QueryResult {
  success: boolean;
  sql_query?: string;
  results?: any[];
  columns?: string[];
  row_count?: number;
  execution_time?: number;
  error?: string;
}

interface QueryOutputProps {
  result: QueryResult | null;
}

export default function QueryOutput({ result }: QueryOutputProps) {
  const [copiedSql, setCopiedSql] = useState(false);
  const [copiedResults, setCopiedResults] = useState(false);

  const copyToClipboard = async (text: string, type: 'sql' | 'results') => {
    await navigator.clipboard.writeText(text);
    if (type === 'sql') {
      setCopiedSql(true);
      setTimeout(() => setCopiedSql(false), 2000);
    } else {
      setCopiedResults(true);
      setTimeout(() => setCopiedResults(false), 2000);
    }
  };

  if (!result) {
    return (
      <Card className="h-full flex items-center justify-center">
        <CardContent className="text-center text-muted-foreground">
          <Database className="h-16 w-16 mx-auto mb-4 opacity-50" />
          <p>Your query results will appear here</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            {result.success ? (
              <>
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                Query Successful
              </>
            ) : (
              <>
                <XCircle className="h-5 w-5 text-red-500" />
                Query Failed
              </>
            )}
          </CardTitle>
          {result.execution_time && (
            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <Clock className="h-4 w-4" />
              {result.execution_time}s
            </div>
          )}
        </div>
        <CardDescription>
          {result.row_count !== undefined && `${result.row_count} rows returned`}
        </CardDescription>
      </CardHeader>
      
      <CardContent className="flex-1 overflow-auto space-y-4">
        {/* SQL Query Section */}
        {result.sql_query && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold">Generated SQL</h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(result.sql_query!, 'sql')}
              >
                {copiedSql ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </Button>
            </div>
            <div className="rounded-md overflow-hidden">
              <SyntaxHighlighter
                language="sql"
                style={oneDark}
                customStyle={{
                  margin: 0,
                  padding: '1rem',
                  fontSize: '0.875rem',
                }}
              >
                {result.sql_query}
              </SyntaxHighlighter>
            </div>
          </div>
        )}

        {/* Error Section */}
        {result.error && (
          <div className="p-4 rounded-md bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-900">
            <p className="text-sm text-red-800 dark:text-red-200 font-mono">
              {result.error}
            </p>
          </div>
        )}

        {/* Results Table */}
        {result.success && result.results && result.results.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold">Results</h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(JSON.stringify(result.results, null, 2), 'results')}
              >
                {copiedResults ? (
                  <Check className="h-4 w-4" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </Button>
            </div>
            <div className="border rounded-md overflow-auto">
              <table className="w-full text-sm">
                <thead className="bg-muted">
                  <tr>
                    {result.columns?.map((column, index) => (
                      <th
                        key={index}
                        className="px-4 py-2 text-left font-medium"
                      >
                        {column}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.results.map((row, rowIndex) => (
                    <tr
                      key={rowIndex}
                      className="border-t hover:bg-muted/50"
                    >
                      {result.columns?.map((column, colIndex) => (
                        <td
                          key={colIndex}
                          className="px-4 py-2"
                        >
                          {row[column] !== null && row[column] !== undefined
                            ? String(row[column])
                            : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Empty Results */}
        {result.success && result.results && result.results.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            <p>No results found</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
