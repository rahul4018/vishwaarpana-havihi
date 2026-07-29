export interface Pooja {
  id: string;

  temple_id: string;
  category_id: string;
  priest_id: string | null;

  name: string;
  slug: string;
  description: string | null;

  duration_minutes: number;
  price: number;
  max_participants: number;

  online_booking: boolean;
  is_active: boolean;
}

export type PoojaListResponse = Pooja[];

export interface CreatePoojaRequest {
  temple_id: string;
  category_id: string;
  priest_id?: string | null;

  name: string;
  slug: string;
  description?: string;

  duration_minutes: number;
  price: number;
  max_participants: number;

  online_booking: boolean;
}

export interface UpdatePoojaRequest {
  category_id?: string;
  priest_id?: string | null;

  name?: string;
  slug?: string;
  description?: string;

  duration_minutes?: number;
  price?: number;
  max_participants?: number;

  online_booking?: boolean;
  is_active?: boolean;
}