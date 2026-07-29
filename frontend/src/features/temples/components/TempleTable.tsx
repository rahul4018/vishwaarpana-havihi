"use client";

import Link from "next/link";
import { toast } from "sonner";

import DeleteConfirmationDialog from "@/components/shared/DeleteConfirmationDialog";

import { useDeleteTemple } from "../hooks/useDeleteTemple";
import type { Temple } from "../types/temple.types";

interface TempleTableProps {
  temples: Temple[];
}

export default function TempleTable({
  temples,
}: TempleTableProps) {
  const deleteTemple = useDeleteTemple();

  async function handleDelete(id: string) {
    try {
      await deleteTemple.mutateAsync(id);

      toast.success("Temple deleted successfully.");
    } catch (error) {
      console.error(error);

      toast.error("Failed to delete temple.");
    }
  }

  return (
    <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
      <table className="min-w-full">
        <thead className="border-b bg-gray-100">
          <tr>
            <th className="p-4 text-left font-semibold">
              Temple
            </th>

            <th className="p-4 text-left font-semibold">
              City
            </th>

            <th className="p-4 text-left font-semibold">
              State
            </th>

            <th className="p-4 text-left font-semibold">
              Country
            </th>

            <th className="p-4 text-left font-semibold">
              Status
            </th>

            <th className="p-4 text-center font-semibold">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {temples.length > 0 ? (
            temples.map((temple) => (
              <tr
                key={temple.id}
                className="border-b transition-colors hover:bg-gray-50"
              >
                <td className="p-4">
                  <Link
                    href={`/temples/${temple.id}`}
                    className="font-medium text-orange-600 hover:underline"
                  >
                    {temple.name}
                  </Link>
                </td>

                <td className="p-4">
                  {temple.city}
                </td>

                <td className="p-4">
                  {temple.state}
                </td>

                <td className="p-4">
                  {temple.country}
                </td>

                <td className="p-4">
                  <span
                    className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${
                      temple.is_active
                        ? "bg-green-100 text-green-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {temple.is_active
                      ? "Active"
                      : "Inactive"}
                  </span>
                </td>

                <td className="p-4">
                  <div className="flex items-center justify-center gap-2">
                    <Link
                      href={`/temples/${temple.id}`}
                      className="rounded-md bg-gray-100 px-3 py-1.5 text-sm font-medium text-gray-700 transition hover:bg-gray-200"
                    >
                      View
                    </Link>

                    <Link
                      href={`/temples/${temple.id}/edit`}
                      className="rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-blue-700"
                    >
                      Edit
                    </Link>

                    <DeleteConfirmationDialog
                      title="Delete Temple"
                      description={`Are you sure you want to delete "${temple.name}"? This action cannot be undone.`}
                      loading={deleteTemple.isPending}
                      onConfirm={() => handleDelete(temple.id)}
                    >
                      <button
                        type="button"
                        className="rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50"
                        disabled={deleteTemple.isPending}
                      >
                        {deleteTemple.isPending
                          ? "Deleting..."
                          : "Delete"}
                      </button>
                    </DeleteConfirmationDialog>
                  </div>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={6}
                className="p-10 text-center text-gray-500"
              >
                No temples found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}