"use client";

import { use } from "react";
import Link from "next/link";

import { useTemple } from "@/features/temples/hooks/useTemple";

interface PageProps {
  params: Promise<{
    id: string;
  }>;
}

export default function TempleDetailsPage({
  params,
}: PageProps) {
  const { id } = use(params);

  const {
    data: temple,
    isLoading,
    isError,
  } = useTemple(id);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-10">
        <p className="text-gray-500">Loading temple...</p>
      </div>
    );
  }

  if (isError || !temple) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6">
        <h2 className="text-lg font-semibold text-red-700">
          Temple not found
        </h2>

        <p className="mt-2 text-sm text-red-600">
          The requested temple could not be found.
        </p>

        <Link
          href="/temples"
          className="mt-4 inline-block rounded-lg bg-gray-800 px-4 py-2 text-white"
        >
          Back to Temples
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            {temple.name}
          </h1>

          <p className="mt-1 text-gray-500">
            Temple Details
          </p>
        </div>

        <div className="flex gap-3">
          <Link
            href={`/temples/${temple.id}/edit`}
            className="rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Edit
          </Link>

          <Link
            href="/temples"
            className="rounded-lg border px-4 py-2 hover:bg-gray-100"
          >
            Back
          </Link>
        </div>
      </div>

      <div className="grid gap-6 rounded-xl border bg-white p-6 shadow-sm md:grid-cols-2">

        <div>
          <p className="text-sm text-gray-500">Temple Name</p>
          <p className="font-medium">{temple.name}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Slug</p>
          <p className="font-medium">{temple.slug}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Email</p>
          <p>{temple.email || "-"}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Phone</p>
          <p>{temple.phone || "-"}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Website</p>
          <p>{temple.website || "-"}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Status</p>
          <span
            className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${
              temple.is_active
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {temple.is_active ? "Active" : "Inactive"}
          </span>
        </div>

        <div className="md:col-span-2">
          <p className="text-sm text-gray-500">Description</p>
          <p>{temple.description || "-"}</p>
        </div>

        <div className="md:col-span-2">
          <p className="text-sm text-gray-500">Address</p>
          <p>{temple.address}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">City</p>
          <p>{temple.city}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">State</p>
          <p>{temple.state}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Country</p>
          <p>{temple.country}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Postal Code</p>
          <p>{temple.postal_code || "-"}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Latitude</p>
          <p>{temple.latitude || "-"}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500">Longitude</p>
          <p>{temple.longitude || "-"}</p>
        </div>
      </div>
    </div>
  );
}