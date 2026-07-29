"use client";

import { useRouter } from "next/navigation";

import TempleForm from "@/features/temples/components/TempleForm";
import { useCreateTemple } from "@/features/temples/hooks/useCreateTemple";
import type { TempleFormValues } from "@/features/temples/validation/temple.schema";

export default function NewTemplePage() {
  const router = useRouter();

  const createTemple = useCreateTemple();

  async function handleSubmit(
    values: TempleFormValues
  ) {
    try {
      await createTemple.mutateAsync(values);

      router.push("/temples");
    } catch (error) {
      console.error(error);
      alert("Unable to create temple.");
    }
  }

  return (
    <div className="max-w-4xl space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          Create Temple
        </h1>

        <p className="text-gray-500">
          Fill in the temple details.
        </p>
      </div>

      <TempleForm
        onSubmit={handleSubmit}
        loading={createTemple.isPending}
      />
    </div>
  );
}