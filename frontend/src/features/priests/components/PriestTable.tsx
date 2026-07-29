"use client";

import Link from "next/link";
import { Eye, Pencil, Trash2 } from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import DeleteConfirmationDialog from "@/components/shared/DeleteConfirmationDialog";

import { Priest } from "../types/priest.types";
import { useDeletePriest } from "../hooks/usePriests";

interface PriestTableProps {
  priests: Priest[];
}

export default function PriestTable({
  priests,
}: PriestTableProps) {
  const deleteMutation = useDeletePriest();

  async function handleDelete(id: string) {
    try {
      await deleteMutation.mutateAsync(id);
      toast.success("Priest deleted successfully");
    } catch {
      toast.error("Failed to delete priest");
    }
  }

  if (priests.length === 0) {
    return (
      <div className="rounded-lg border bg-card p-10 text-center text-muted-foreground">
        No priests found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border bg-background">
      <table className="w-full">
        <thead className="border-b bg-muted/50">
          <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Phone</th>
            <th className="px-4 py-3 text-left">Email</th>
            <th className="px-4 py-3 text-left">Experience</th>
            <th className="px-4 py-3 text-left">Status</th>
            <th className="px-4 py-3 text-right">Actions</th>
          </tr>
        </thead>

        <tbody>
          {priests.map((priest) => (
            <tr
              key={priest.id}
              className="border-b last:border-none"
            >
              <td className="px-4 py-3 font-medium">
                {priest.full_name}
              </td>

              <td className="px-4 py-3">
                {priest.phone}
              </td>

              <td className="px-4 py-3">
                {priest.email ?? "-"}
              </td>

              <td className="px-4 py-3">
                {priest.experience_years} Years
              </td>

              <td className="px-4 py-3">
                <Badge
                  variant={
                    priest.is_active
                      ? "default"
                      : "secondary"
                  }
                >
                  {priest.is_active
                    ? "Active"
                    : "Inactive"}
                </Badge>
              </td>

              <td className="px-4 py-3">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    size="icon"
                    asChild
                  >
                    <Link href={`/priests/${priest.id}`}>
                      <Eye className="h-4 w-4" />
                    </Link>
                  </Button>

                  <Button
                    variant="outline"
                    size="icon"
                    asChild
                  >
                    <Link
                      href={`/priests/${priest.id}/edit`}
                    >
                      <Pencil className="h-4 w-4" />
                    </Link>
                  </Button>

                  <DeleteConfirmationDialog
                    title="Delete Priest"
                    description={`Are you sure you want to delete "${priest.full_name}"?`}
                    onConfirm={() =>
                      handleDelete(priest.id)
                    }
                    loading={deleteMutation.isPending}
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