export type UserRole =
  | "SUPER_ADMIN"
  | "ADMIN"
  | "TEMPLE_ADMIN"
  | "PRIEST"
  | "DEVOTEE";

export interface User {
  id: string;
  full_name: string;
  email: string;
  role: UserRole;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  full_name: string;
  email: string;
  password: string;
  mobile: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
}

export interface LoginResponse {
  user: User;
  tokens: TokenResponse;
}

export interface RefreshResponse {
  access_token: string;
  token_type: "bearer";
}