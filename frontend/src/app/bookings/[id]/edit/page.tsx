"use client";

import { notFound, useParams } from "next/navigation";

import BookingForm from "@/features/bookings/components/BookingForm";
import { useBooking } from "@/features/bookings/hooks/useBookings";

export default function EditBookingPage() {
  const params = useParams();

  const {
    data: booking,
    isLoading,
    error,
  } = useBooking(params.id as string);

  if (isLoading) {
    return (
      <div className="container mx-auto py-6">
        Loading...
      </div>
    );
  }

  if (error || !booking) {
    notFound();
  }

  return (
    <div className="container mx-auto max-w-5xl py-6">
      <BookingForm booking={booking} />
    </div>
  );
}