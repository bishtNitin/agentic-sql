'use client';

import { useState } from 'react';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Send, Loader2, Lightbulb } from 'lucide-react';

interface QueryInputProps {
  onSubmit: (query: string) => void;
  isLoading: boolean;
}

const EXAMPLE_QUERIES = [
  "Show all employees",
  "Find employees with salary greater than 60000",
  "Count employees by department",
  "Show top 5 products by price",
  "List all customers from New York",
  "Show average salary by department",
];

export default function QueryInput({ onSubmit, isLoading }: QueryInputProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query.trim());
    }
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle>Natural Language Query</CardTitle>
        <CardDescription>
          Ask a question in plain English and we'll convert it to SQL
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col gap-4">
        <form onSubmit={handleSubmit} className="flex-1 flex flex-col gap-4">
          <Textarea
            placeholder="E.g., Show me all employees with salary greater than 50000"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 resize-none min-h-[150px]"
            disabled={isLoading}
          />
          
          <Button 
            type="submit" 
            disabled={!query.trim() || isLoading}
            className="w-full"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4" />
                Execute Query
              </>
            )}
          </Button>
        </form>

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Lightbulb className="h-4 w-4" />
            Example Queries
          </div>
          <div className="grid grid-cols-1 gap-2">
            {EXAMPLE_QUERIES.map((example, index) => (
              <button
                key={index}
                onClick={() => handleExampleClick(example)}
                disabled={isLoading}
                className="text-left text-sm px-3 py-2 rounded-md border border-border hover:bg-accent hover:text-accent-foreground transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
