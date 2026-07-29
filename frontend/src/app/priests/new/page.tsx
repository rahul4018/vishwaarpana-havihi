"use client";

import PageHeader from "@/components/shared/PageHeader";
import PriestForm from "@/features/priests/components/PriestForm";

export default function NewPriestPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Add Priest"
        description="Create a new priest"
      />

      <PriestForm />
    </div>
  );
}