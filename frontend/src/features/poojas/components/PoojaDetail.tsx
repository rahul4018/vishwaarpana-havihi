"use client";

import { Badge } from "@/components/ui/badge";

import type { Pooja } from "../types/pooja.types";

interface Props {
  pooja: Pooja;
}

export default function PoojaDetail({
  pooja,
}: Props) {
  return (
    <div className="rounded-lg border bg-card p-6 space-y-5">
      <div>
        <h2 className="text-2xl font-bold">
          {pooja.name}
        </h2>

        <p className="text-muted-foreground">
          {pooja.slug}
        </p>
      </div>

      <div>
        <strong>Description</strong>

        <p className="mt-1">
          {pooja.description || "-"}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <strong>Duration</strong>

          <p>
            {pooja.duration_minutes} Minutes
          </p>
        </div>

        <div>
          <strong>Price</strong>

          <p>₹{pooja.price}</p>
        </div>

        <div>
          <strong>Participants</strong>

          <p>{pooja.max_participants}</p>
        </div>

        <div>
          <strong>Online Booking</strong>

          <p>
            {pooja.online_booking
              ? "Enabled"
              : "Disabled"}
          </p>
        </div>
      </div>

      <div>
        <Badge
          variant={
            pooja.is_active
              ? "default"
              : "secondary"
          }
        >
          {pooja.is_active
            ? "Active"
            : "Inactive"}
        </Badge>
      </div>
    </div>
  );
}