"use client";

import Link from "next/link";
import {
  Eye,
  Pencil,
  Trash2,
} from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import DeleteConfirmationDialog from "@/components/shared/DeleteConfirmationDialog";

import { useDeletePriestAvailability } from "../hooks/usePriestAvailability";

import type { PriestAvailability } from "../types/priestAvailability.types";

interface Props {
  availability: PriestAvailability[];
}

export default function AvailabilityTable({
  availability,
}: Props) {
  const deleteMutation =
    useDeletePriestAvailability();

  async function handleDelete(
    id: string
  ) {
    try {
      await deleteMutation.mutateAsync(
        id
      );

      toast.success(
        "Availability deleted successfully"
      );
    } catch {
      toast.error(
        "Failed to delete availability"
      );
    }
  }

  if (availability.length === 0) {
    return (
      <div className="rounded-lg border bg-card p-10 text-center text-muted-foreground">
        No availability records found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border bg-background">
      <table className="w-full">
        <thead className="border-b bg-muted/50">
          <tr>
            <th className="px-4 py-3 text-left">
              Priest ID
            </th>

            <th className="px-4 py-3 text-left">
              Date
            </th>

            <th className="px-4 py-3 text-left">
              Start Time
            </th>

            <th className="px-4 py-3 text-left">
              End Time
            </th>

            <th className="px-4 py-3 text-left">
              Status
            </th>

            <th className="px-4 py-3 text-left">
              Remarks
            </th>

            <th className="px-4 py-3 text-right">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {availability.map((item) => (
            <tr
              key={item.id}
              className="border-b last:border-none"
            >
              <td className="px-4 py-3 font-mono text-xs">
                {item.priest_id}
              </td>

              <td className="px-4 py-3">
                {item.available_date}
              </td>

              <td className="px-4 py-3">
                {item.start_time}
              </td>

              <td className="px-4 py-3">
                {item.end_time}
              </td>

              <td className="px-4 py-3">
                <Badge
                  variant={
                    item.is_available
                      ? "default"
                      : "secondary"
                  }
                >
                  {item.is_available
                    ? "Available"
                    : "Unavailable"}
                </Badge>
              </td>

              <td className="px-4 py-3 max-w-xs truncate">
                {item.remarks || "-"}
              </td>

              <td className="px-4 py-3">
                <div className="flex justify-end gap-2">
                  <Button
                    asChild
                    variant="outline"
                    size="icon"
                  >
                    <Link
                      href={`/priest-availability/${item.id}`}
                    >
                      <Eye className="h-4 w-4" />
                    </Link>
                  </Button>

                  <Button
                    asChild
                    variant="outline"
                    size="icon"
                  >
                    <Link
                      href={`/priest-availability/${item.id}/edit`}
                    >
                      <Pencil className="h-4 w-4" />
                    </Link>
                  </Button>

                  <DeleteConfirmationDialog
                    title="Delete Availability"
                    description="Are you sure you want to delete this availability record?"
                    loading={
                      deleteMutation.isPending
                    }
                    onConfirm={() =>
                      handleDelete(item.id)
                    }
                  >
                    <Button
                      variant="destructive"
                      size="icon"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </DeleteConfirmationDialog>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}