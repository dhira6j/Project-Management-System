import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { ThemeProvider, useTheme } from '@/contexts/ThemeContext'; // Import ThemeProvider
import { Moon, Sun } from 'lucide-react';


const ModeToggle = () => {
  const { theme, setTheme } = useTheme();
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="absolute top-4 right-4"
    >
      <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}

const HomePage: React.FC = () => {
  return (
    // Wrap HomePage content with ThemeProvider if it's a standalone page or root for theme
    // If App.tsx wraps everything, this might not be needed here.
    // For now, let's assume App.tsx will handle the main ThemeProvider for global theme.
    // The DashboardLayout has its own ThemeProvider, which is fine for that section.
    // This toggle is just for demonstrating it on the homepage.
      <div className="min-h-screen flex flex-col items-center justify-center bg-background p-4">
        <ModeToggle />
        <h1 className="text-4xl font-bold mb-8 text-foreground">Welcome to Project Management Platform</h1>
        <div className="space-x-4">
          <Button asChild>
            <Link to="/login">Login</Link>
          </Button>
          <Button variant="secondary" asChild>
            <Link to="/register">Register</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link to="/dashboard">Go to Dashboard (Dev)</Link>
          </Button>
        </div>
      </div>
  );
};

// Wrap HomePage with ThemeProvider if it's intended to be a root for theme context
const HomePageWithTheme: React.FC = () => (
  <ThemeProvider defaultTheme='system' storageKey='vite-ui-theme-home'>
    <HomePage />
  </ThemeProvider>
)

export default HomePageWithTheme;
