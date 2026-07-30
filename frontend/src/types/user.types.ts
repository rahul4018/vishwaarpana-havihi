export interface User {
  id: string;
  full_name: string;
  email: string;
  mobile: string | null;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateUserRequest {
  full_name: string;
  email: string;
  mobile?: string;
  password: string;
  role_id: string;
}

export interface UpdateUserRequest {
  full_name?: string;
  mobile?: string;
  role_id?: string;
  is_active?: boolean;
  is_verified?: boolean;
}