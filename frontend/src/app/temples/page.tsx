"use client";

import Link from "next/link";

import TempleTable from "@/features/temples/components/TempleTable";
import { useTemples } from "@/features/temples/hooks/useTemples";

export default function TemplesPage() {
  const {
    data,
    isLoading,
    isError,
    error,
  } = useTemples();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-10">
        <p className="text-gray-500">
          Loading temples...
        </p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6">
        <h2 className="text-lg font-semibold text-red-700">
          Failed to load temples
        </h2>

        <p className="mt-2 text-sm text-red-600">
          {error instanceof Error
            ? error.message
            : "Something went wrong."}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Temples
          </h1>

          <p className="mt-1 text-gray-500">
            Manage all temples in the system.
          </p>
        </div>

        <Link
          href="/temples/new"
          className="rounded-lg bg-orange-500 px-4 py-2 text-white transition hover:bg-orange-600"
        >
          Add Temple
        </Link>
      </div>

      <TempleTable temples={data ?? []} />
    </div>
  );
}