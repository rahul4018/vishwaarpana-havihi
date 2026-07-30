"use client";

import Link from "next/link";
import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

import BookingTable from "@/features/bookings/components/BookingTable";
import { useBookings } from "@/features/bookings/hooks/useBookings";

export default function BookingsPage() {
  const {
    data: bookings = [],
    isLoading,
    error,
  } = useBookings();

  if (isLoading) {
    return (
      <div className="p-6">
        Loading bookings...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-500">
        Failed to load bookings.
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Bookings
          </h1>

          <p className="text-muted-foreground">
            Manage all temple bookings.
          </p>
        </div>

        <Button asChild>
          <Link href="/bookings/new">
            <Plus className="mr-2 h-4 w-4" />
            New Booking
          </Link>
        </Button>
      </div>

      <BookingTable bookings={bookings} />
    </div>
  );
}