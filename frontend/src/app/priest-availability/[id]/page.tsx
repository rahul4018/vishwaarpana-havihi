"use client";

import { notFound } from "next/navigation";

import AvailabilityDetail from "@/features/priest-availability/components/AvailabilityDetail";

import { usePriestAvailabilityById } from "@/features/priest-availability/hooks/usePriestAvailability";

interface Props {
  params: {
    id: string;
  };
}

export default function AvailabilityDetailsPage({
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
    <AvailabilityDetail
      availability={data}
    />
  );
}