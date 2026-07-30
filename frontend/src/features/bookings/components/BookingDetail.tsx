"use client";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

import type { Booking } from "../types/booking.types";

interface Props {
  booking: Booking;
}

export default function BookingDetail({
  booking,
}: Props) {
  return (
    <Card>
      <CardContent className="space-y-6 pt-6">

        <div className="grid grid-cols-2 gap-6">

          <div>
            <h3 className="font-semibold">
              Booking Number
            </h3>

            <p>{booking.booking_number}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Devotee
            </h3>

            <p>{booking.devotee_name}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Mobile
            </h3>

            <p>{booking.devotee_mobile}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Email
            </h3>

            <p>{booking.devotee_email}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Booking Date
            </h3>

            <p>{booking.booking_date}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Booking Time
            </h3>

            <p>{booking.booking_time}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Participants
            </h3>

            <p>{booking.participants}</p>
          </div>

          <div>
            <h3 className="font-semibold">
              Booking Status
            </h3>

            <Badge>
              {booking.booking_status}
            </Badge>
          </div>

          <div>
            <h3 className="font-semibold">
              Payment Status
            </h3>

            <Badge variant="secondary">
              {booking.payment_status}
            </Badge>
          </div>

        </div>

        {booking.special_notes && (
          <div>
            <h3 className="font-semibold">
              Special Notes
            </h3>

            <p>{booking.special_notes}</p>
          </div>
        )}

      </CardContent>
    </Card>
  );
}