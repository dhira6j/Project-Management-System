export interface User {
  id: number;
  email: string;
  full_name?: string | null;
  role: string; // Consider using an enum shared with backend if possible
  is_active: boolean;
  is_verified: boolean;
  // consultant_profile?: any; // Add later if needed
}

export interface UserCreate {
  email: string;
  password: string;
  full_name?: string;
  role?: string; // e.g., 'consultant', 'project_manager'
}
