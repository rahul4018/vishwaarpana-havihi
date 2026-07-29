"use client";

import { useParams } from "next/navigation";

import PageHeader from "@/components/shared/PageHeader";

import PoojaDetail from "@/features/poojas/components/PoojaDetail";
import { usePooja } from "@/features/poojas/hooks/usePoojas";

export default function PoojaPage() {
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
        title={pooja.name}
        description="Pooja Details"
      />

      <PoojaDetail pooja={pooja} />
    </div>
  );
}