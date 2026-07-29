export interface Temple {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  email: string | null;
  phone: string | null;
  website: string | null;
  address: string;
  city: string;
  state: string;
  country: string;
  postal_code: string | null;
  latitude: string | null;
  longitude: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export type TempleListResponse = Temple[];

export interface CreateTempleRequest {
  name: string;
  slug: string;
  description?: string;
  email?: string;
  phone?: string;
  website?: string;
  address: string;
  city: string;
  state: string;
  country: string;
  postal_code?: string;
  latitude?: string;
  longitude?: string;
}

export interface UpdateTempleRequest
  extends Partial<CreateTempleRequest> {
  is_active?: boolean;
}