"use client";

import { notFound } from "next/navigation";

import AvailabilityForm from "@/features/priest-availability/components/AvailabilityForm";

import { usePriestAvailabilityById } from "@/features/priest-availability/hooks/usePriestAvailability";

interface Props {
  params: {
    id: string;
  };
}

export default function EditAvailabilityPage({
  params,
}: Props) {
  const {
    data,
    isLoading,
    error,
  } = usePriestAvailabilityById(
    params.id
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error || !data) {
    notFound();
  }

  return (
    <AvailabilityForm
      availability={data}
    />
  );
}