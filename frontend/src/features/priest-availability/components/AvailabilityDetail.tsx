"use client";

import Link from "next/link";

import { ArrowLeft, Pencil } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import type { PriestAvailability } from "../types/priestAvailability.types";

interface Props {
  availability: PriestAvailability;
}

export default function AvailabilityDetail({
  availability,
}: Props) {
  return (
    <div className="space-y-6">

      <div className="flex items-center justify-between">

        <Button
          asChild
          variant="outline"
        >
          <Link href="/priest-availability">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Link>
        </Button>

        <Button asChild>
          <Link
            href={`/priest-availability/${availability.id}/edit`}
          >
            <Pencil className="mr-2 h-4 w-4" />
            Edit
          </Link>
        </Button>

      </div>

      <Card>

        <CardHeader>
          <CardTitle>
            Availability Details
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">

          <div>
            <p className="text-sm text-muted-foreground">
              Priest ID
            </p>

            <p className="font-medium">
              {availability.priest_id}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Date
            </p>

            <p className="font-medium">
              {availability.available_date}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Start Time
            </p>

            <p className="font-medium">
              {availability.start_time}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              End Time
            </p>

            <p className="font-medium">
              {availability.end_time}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Status
            </p>

            <Badge
              variant={
                availability.is_available
                  ? "default"
                  : "destructive"
              }
            >
              {availability.is_available
                ? "Available"
                : "Unavailable"}
            </Badge>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Remarks
            </p>

            <p>
              {availability.remarks ||
                "-"}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Created At
            </p>

            <p>
              {new Date(
                availability.created_at
              ).toLocaleString()}
            </p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground">
              Updated At
            </p>

            <p>
              {new Date(
                availability.updated_at
              ).toLocaleString()}
            </p>
          </div>

        </CardContent>

      </Card>

    </div>
  );
}