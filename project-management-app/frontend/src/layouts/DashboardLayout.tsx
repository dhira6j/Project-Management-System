import React from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { ThemeProvider, useTheme } from '@/contexts/ThemeContext'; // ThemeProvider is not strictly needed here if App.tsx has global one
import { Button } from '@/components/ui/button';
import { Moon, Sun, LogOut, UserCircle } from 'lucide-react'; // Added LogOut, UserCircle
import { useAuth } from '@/contexts/AuthContext'; // Import useAuth
import { cn } from "@/lib/utils"; // For NavLink active class
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";


const Header: React.FC = () => {
  const { theme, setTheme } = useTheme();
  const { user, logout } = useAuth(); // Get user and logout from AuthContext
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login'); // Redirect to login after logout
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <Link to="/dashboard" className="mr-6 flex items-center space-x-2">
          {/* <img src="/logo.svg" alt="Logo" className="h-6 w-6" /> Placeholder for logo */}
          <span className="font-bold sm:inline-block">ProjectPlatform</span>
        </Link>
        {/* <nav className="flex items-center space-x-6 text-sm font-medium">
          {/* Nav links here later */}
        {/* </nav> */}
        <div className="flex flex-1 items-center justify-end space-x-2 md:space-x-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          >
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
          {user ? (
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                  <UserCircle className="h-6 w-6" /> {/* Or use an Avatar component */}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{user.full_name || user.email}</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {user.email} ({user.role})
                    </p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={() => navigate('/dashboard/profile')}> {/* Placeholder profile link */}
                  Profile
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => navigate('/dashboard/settings')}> {/* Placeholder settings link */}
                  Settings
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem onClick={handleLogout} className="text-red-600 focus:text-red-600 focus:bg-red-50 dark:focus:bg-red-700/20">
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          ) : (
            <Button asChild variant="outline">
              <Link to="/login">Login</Link>
            </Button>
          )}
        </div>
      </div>
    </header>
  );
};

const Sidebar: React.FC = () => {
  const { user } = useAuth();
  // Example of using NavLink from react-router-dom if needed for active class styling,
  // but here we use a simple Link and a manual active check with a helper or inline.
  // For simplicity, a basic Link is used. `cn` is for conditional classes.
  // `isActive` prop is not directly available for `Link`. If NavLink is preferred, install and use it.
  return (
    <aside className="fixed top-14 z-30 -ml-2 hidden h-[calc(100vh-3.5rem)] w-full shrink-0 md:sticky md:block overflow-y-auto border-r py-6 pr-6 lg:py-8 lg:pr-6 xl:pr-6">
      <nav className="flex flex-col space-y-1">
        <Link to="/dashboard" className={cn("rounded-md px-3 py-2 text-sm font-medium hover:bg-accent", window.location.pathname === '/dashboard' && "bg-accent text-accent-foreground")}>Dashboard</Link>
        <Link to="/dashboard/projects" className={cn("rounded-md px-3 py-2 text-sm font-medium hover:bg-accent", window.location.pathname.startsWith('/dashboard/projects') && "bg-accent text-accent-foreground")}>Projects</Link>
        {/* Role-specific links */}
        {user?.role === 'admin' && (
          <Link to="/dashboard/admin/users" className={cn("rounded-md px-3 py-2 text-sm font-medium hover:bg-accent", window.location.pathname.startsWith('/dashboard/admin/users') && "bg-accent text-accent-foreground")}>User Management</Link>
        )}
        {/* More links later */}
      </nav>
    </aside>
  );
};

const DashboardLayout: React.FC = () => {
  return (
    // ThemeProvider is global in App.tsx. If DashboardLayout needs its own scope, it can be re-added.
    // For now, relying on the global one from App.tsx.
      <div className="relative flex min-h-screen flex-col bg-background">
        <Header />
        <div className="container flex-1 items-start md:grid md:grid-cols-[200px_minmax(0,1fr)] md:gap-6 lg:grid-cols-[220px_minmax(0,1fr)] lg:gap-8">
          <Sidebar />
          <main className="relative py-6 lg:py-8 md:col-span-1">
            <Outlet /> {/* Child routes will render here */}
          </main>
        </div>
      </div>
  );
};
export default DashboardLayout;
