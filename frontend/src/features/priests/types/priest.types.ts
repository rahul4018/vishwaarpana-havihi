export interface Priest {
  id: string;
  temple_id: string;

  full_name: string;

  email: string | null;

  phone: string;

  experience_years: number;

  specialization: string | null;

  bio: string | null;

  is_active: boolean;
}

export type PriestListResponse = Priest[];

export interface CreatePriestRequest {
  temple_id: string;

  full_name: string;

  email?: string;

  phone: string;

  experience_years: number;

  specialization?: string;

  bio?: string;
}

export interface UpdatePriestRequest {
  full_name?: string;

  email?: string;

  phone?: string;

  experience_years?: number;

  specialization?: string;

  bio?: string;

  is_active?: boolean;
}