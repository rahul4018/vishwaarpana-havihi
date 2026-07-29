"use client";

import Link from "next/link";

import PageHeader from "@/components/shared/PageHeader";
import { Button } from "@/components/ui/button";

import PoojaTable from "@/features/poojas/components/PoojaTable";
import { usePoojas } from "@/features/poojas/hooks/usePoojas";

export default function PoojasPage() {
  const {
    data: poojas = [],
    isLoading,
    isError,
  } = usePoojas();

  if (isLoading) {
    return (
      <div className="p-6">
        Loading poojas...
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-6 text-red-500">
        Failed to load poojas.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Poojas"
        description="Manage temple poojas"
        action={
          <Button asChild>
            <Link href="/poojas/new">
              Add Pooja
            </Link>
          </Button>
        }
      />

      <PoojaTable poojas={poojas} />
    </div>
  );
}