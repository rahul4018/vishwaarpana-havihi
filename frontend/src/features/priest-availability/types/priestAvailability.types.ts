export interface PriestAvailability {
  id: string;
  priest_id: string;
  available_date: string;
  start_time: string;
  end_time: string;
  is_available: boolean;
  remarks?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreatePriestAvailabilityRequest {
  priest_id: string;
  available_date: string;
  start_time: string;
  end_time: string;
  is_available: boolean;
  remarks?: string;
}

export interface UpdatePriestAvailabilityRequest {
  available_date?: string;
  start_time?: string;
  end_time?: string;
  is_available?: boolean;
  remarks?: string;
}