'use client';

import { useState, useEffect } from 'react';
import { Moon, Sun, Database } from 'lucide-react';
import { Button } from './ui/button';

export default function Header() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Check system preference or localStorage
    if (typeof window !== 'undefined') {
      const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null;
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      const initialTheme = savedTheme || systemTheme;
      
      setTheme(initialTheme);
      document.documentElement.classList.toggle('dark', initialTheme === 'dark');
    }
  }, []);

  const toggleTheme = () => {
    if (typeof window !== 'undefined') {
      const newTheme = theme === 'light' ? 'dark' : 'light';
      setTheme(newTheme);
      localStorage.setItem('theme', newTheme);
      document.documentElement.classList.toggle('dark', newTheme === 'dark');
    }
  };

  // Avoid hydration mismatch by not rendering theme toggle until mounted
  if (!mounted) {
    return (
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Database className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-2xl font-bold">Agentic SQL</h1>
              <p className="text-sm text-muted-foreground">
                Natural Language to SQL Agent
              </p>
            </div>
          </div>
          <div className="w-10 h-10" /> {/* Placeholder for theme toggle */}
        </div>
      </header>
    );
  }

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Database className="h-8 w-8 text-primary" />
          <div>
            <h1 className="text-2xl font-bold">Agentic SQL</h1>
            <p className="text-sm text-muted-foreground">
              Natural Language to SQL Agent
            </p>
          </div>
        </div>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={toggleTheme}
          aria-label="Toggle theme"
        >
          {theme === 'light' ? (
            <Moon className="h-5 w-5" />
          ) : (
            <Sun className="h-5 w-5" />
          )}
        </Button>
      </div>
    </header>
  );
}
