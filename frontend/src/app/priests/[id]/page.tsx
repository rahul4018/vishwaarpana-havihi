"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { Button } from "@/components/ui/button";
import PageHeader from "@/components/shared/PageHeader";

import { usePriest } from "@/features/priests/hooks/usePriests";

export default function PriestDetailPage() {
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
        title={data.full_name}
        description="Priest Details"
        action={
          <Button asChild>
            <Link href={`/priests/${data.id}/edit`}>
              Edit
            </Link>
          </Button>
        }
      />

      <div className="rounded-lg border p-6 space-y-3">
        <p><strong>Name:</strong> {data.full_name}</p>
        <p><strong>Email:</strong> {data.email || "-"}</p>
        <p><strong>Phone:</strong> {data.phone}</p>
        <p><strong>Experience:</strong> {data.experience_years} Years</p>
        <p><strong>Specialization:</strong> {data.specialization || "-"}</p>
        <p><strong>Bio:</strong> {data.bio || "-"}</p>
        <p>
          <strong>Status:</strong>{" "}
          {data.is_active ? "Active" : "Inactive"}
        </p>
      </div>
    </div>
  );
}