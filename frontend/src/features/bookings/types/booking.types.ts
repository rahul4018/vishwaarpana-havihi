export interface Booking {
  id: string;
  booking_number: string;

  user_id: string;
  temple_id: string;
  pooja_id: string;

  booking_date: string;
  booking_time: string;

  participants: number;

  devotee_name: string;
  devotee_mobile: string;
  devotee_email: string;

  special_notes: string | null;

  booking_status: string;
  payment_status: string;

  created_at: string;
  updated_at: string;
}

export type BookingListResponse = Booking[];

export interface CreateBookingRequest {
  temple_id: string;
  pooja_id: string;

  booking_date: string;
  booking_time: string;

  participants: number;

  devotee_name: string;
  devotee_mobile: string;
  devotee_email: string;

  special_notes?: string;
}

export interface UpdateBookingRequest {
  booking_date?: string;
  booking_time?: string;

  participants?: number;

  devotee_name?: string;
  devotee_mobile?: string;
  devotee_email?: string;

  special_notes?: string;

  payment_status?: string;
}