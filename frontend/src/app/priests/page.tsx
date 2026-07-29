"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";
import PageHeader from "@/components/shared/PageHeader";

import PriestTable from "@/features/priests/components/PriestTable";
import { usePriests } from "@/features/priests/hooks/usePriests";

export default function PriestsPage() {
  const {
    data: priests = [],
    isLoading,
    isError,
  } = usePriests();

  if (isLoading) {
    return (
      <div className="p-6">
        Loading priests...
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-6 text-red-500">
        Failed to load priests.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Priests"
        description="Manage temple priests"
        action={
          <Button asChild>
            <Link href="/priests/new">
              Add Priest
            </Link>
          </Button>
        }
      />

      <PriestTable priests={priests} />
    </div>
  );
}