"use client";

import { useParams } from "next/navigation";

import PageHeader from "@/components/shared/PageHeader";
import PriestForm from "@/features/priests/components/PriestForm";
import { usePriest } from "@/features/priests/hooks/usePriests";

export default function EditPriestPage() {
  const { id } = useParams<{ id: string }>();

  const { data, isLoading } = usePriest(id);

  if (isLoading) {
    return <div className="p-6">Loading...</div>;
  }

  if (!data) {
    return <div className="p-6">Priest not found.</div>;
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Priest"
        description="Update priest information"
      />

      <PriestForm priest={data} />
    </div>
  );
}