"use client";

import { notFound, useParams } from "next/navigation";

import BookingDetail from "@/features/bookings/components/BookingDetail";
import { useBooking } from "@/features/bookings/hooks/useBookings";

export default function BookingPage() {
  const params = useParams();

  const {
    data: booking,
    isLoading,
    error,
  } = useBooking(params.id as string);

  if (isLoading) {
    return <div className="p-6">Loading...</div>;
  }

  if (error || !booking) {
    notFound();
  }

  return (
    <div className="container mx-auto max-w-5xl py-6">
      <BookingDetail booking={booking} />
    </div>
  );
}