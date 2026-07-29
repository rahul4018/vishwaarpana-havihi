"use client";

import { useParams } from "next/navigation";

import PageHeader from "@/components/shared/PageHeader";

import PoojaForm from "@/features/poojas/components/PoojaForm";
import { usePooja } from "@/features/poojas/hooks/usePoojas";

export default function EditPoojaPage() {
  const params = useParams();

  const {
    data: pooja,
    isLoading,
    isError,
  } = usePooja(params.id as string);

  if (isLoading) {
    return (
      <div className="p-6">
        Loading...
      </div>
    );
  }

  if (isError || !pooja) {
    return (
      <div className="p-6 text-red-500">
        Pooja not found.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Pooja"
        description="Update pooja details"
      />

      <PoojaForm pooja={pooja} />
    </div>
  );
}