"use client";

import Link from "next/link";
import {
  Eye,
  Pencil,
  Trash2,
} from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import DeleteConfirmationDialog from "@/components/shared/DeleteConfirmationDialog";

import { useDeleteBooking } from "../hooks/useBookings";

import type { Booking } from "../types/booking.types";

interface BookingTableProps {
  bookings: Booking[];
}

export default function BookingTable({
  bookings,
}: BookingTableProps) {
  const deleteMutation =
    useDeleteBooking();

  async function handleDelete(
    id: string
  ) {
    try {
      await deleteMutation.mutateAsync(
        id
      );

      toast.success(
        "Booking deleted successfully"
      );
    } catch {
      toast.error(
        "Failed to delete booking"
      );
    }
  }

  if (bookings.length === 0) {
    return (
      <div className="rounded-lg border bg-card p-10 text-center text-muted-foreground">
        No bookings found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border bg-background">
      <table className="w-full">
        <thead className="border-b bg-muted/50">
          <tr>
            <th className="px-4 py-3 text-left">
              Booking No
            </th>

            <th className="px-4 py-3 text-left">
              Devotee
            </th>

            <th className="px-4 py-3 text-left">
              Mobile
            </th>

            <th className="px-4 py-3 text-left">
              Date
            </th>

            <th className="px-4 py-3 text-left">
              Time
            </th>

            <th className="px-4 py-3 text-left">
              Participants
            </th>

            <th className="px-4 py-3 text-left">
              Booking
            </th>

            <th className="px-4 py-3 text-left">
              Payment
            </th>

            <th className="px-4 py-3 text-right">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {bookings.map(
            (booking) => (
              <tr
                key={booking.id}
                className="border-b last:border-none"
              >
                <td className="px-4 py-3 font-medium">
                  {
                    booking.booking_number
                  }
                </td>

                <td className="px-4 py-3">
                  {
                    booking.devotee_name
                  }
                </td>

                <td className="px-4 py-3">
                  {
                    booking.devotee_mobile
                  }
                </td>

                <td className="px-4 py-3">
                  {
                    booking.booking_date
                  }
                </td>

                <td className="px-4 py-3">
                  {
                    booking.booking_time
                  }
                </td>

                <td className="px-4 py-3">
                  {
                    booking.participants
                  }
                </td>

                <td className="px-4 py-3">
                  <Badge
                    variant={
                      booking.booking_status ===
                      "CONFIRMED"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {
                      booking.booking_status
                    }
                  </Badge>
                </td>

                <td className="px-4 py-3">
                  <Badge
                    variant={
                      booking.payment_status ===
                      "PAID"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {
                      booking.payment_status
                    }
                  </Badge>
                </td>

                <td className="px-4 py-3">
                  <div className="flex justify-end gap-2">
                                        <Button
                      asChild
                      variant="outline"
                      size="icon"
                    >
                      <Link
                        href={`/bookings/${booking.id}`}
                      >
                        <Eye className="h-4 w-4" />
                      </Link>
                    </Button>

                    <Button
                      asChild
                      variant="outline"
                      size="icon"
                    >
                      <Link
                        href={`/bookings/${booking.id}/edit`}
                      >
                        <Pencil className="h-4 w-4" />
                      </Link>
                    </Button>

                    <DeleteConfirmationDialog
                      title="Delete Booking"
                      description={`Are you sure you want to delete booking ${booking.booking_number}?`}
                      onConfirm={() =>
                        handleDelete(
                          booking.id
                        )
                      }
                    >
                      <Button
                        variant="destructive"
                        size="icon"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </DeleteConfirmationDialog>
                  </div>
                </td>
              </tr>
            )
          )}
        </tbody>
      </table>
    </div>
  );
}