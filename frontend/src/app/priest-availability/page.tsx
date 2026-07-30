"use client";

import Link from "next/link";

import { Plus } from "lucide-react";

import { Button } from "@/components/ui/button";

import AvailabilityTable from "@/features/priest-availability/components/AvailabilityTable";
import { usePriestAvailability } from "@/features/priest-availability/hooks/usePriestAvailability";

export default function PriestAvailabilityPage() {
  const {
    data = [],
    isLoading,
    error,
  } = usePriestAvailability();

  if (isLoading) {
    return (
      <div className="p-6">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-500">
        Failed to load availability.
      </div>
    );
  }

  return (
    <div className="space-y-6">

      <div className="flex items-center justify-between">

        <div>
          <h1 className="text-3xl font-bold">
            Priest Availability
          </h1>

          <p className="text-muted-foreground">
            Manage priest availability schedule.
          </p>

        </div>

        <Button asChild>
          <Link href="/priest-availability/new">
            <Plus className="mr-2 h-4 w-4" />
            Add Availability
          </Link>
        </Button>

      </div>

      <AvailabilityTable
        availability={data}
      />

    </div>
  );
}