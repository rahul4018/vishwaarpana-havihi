"use client";

import Link from "next/link";
import { Eye, Pencil, Trash2 } from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import DeleteConfirmationDialog from "@/components/shared/DeleteConfirmationDialog";

import { Pooja } from "../types/pooja.types";
import { useDeletePooja } from "../hooks/usePoojas";

interface Props {
  poojas: Pooja[];
}

export default function PoojaTable({
  poojas,
}: Props) {
  const deleteMutation = useDeletePooja();

  async function handleDelete(id: string) {
    try {
      await deleteMutation.mutateAsync(id);
      toast.success("Pooja deleted successfully");
    } catch {
      toast.error("Failed to delete pooja");
    }
  }

  if (poojas.length === 0) {
    return (
      <div className="rounded-lg border bg-card p-10 text-center text-muted-foreground">
        No poojas found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border bg-background">
      <table className="w-full">
        <thead className="border-b bg-muted/50">
          <tr>
            <th className="px-4 py-3 text-left">Name</th>
            <th className="px-4 py-3 text-left">Price</th>
            <th className="px-4 py-3 text-left">
              Duration
            </th>
            <th className="px-4 py-3 text-left">
              Participants
            </th>
            <th className="px-4 py-3 text-left">
              Online
            </th>
            <th className="px-4 py-3 text-left">
              Status
            </th>
            <th className="px-4 py-3 text-right">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {poojas.map((pooja) => (
            <tr
              key={pooja.id}
              className="border-b last:border-none"
            >
              <td className="px-4 py-3 font-medium">
                {pooja.name}
              </td>

              <td className="px-4 py-3">
                ₹{Number(pooja.price).toFixed(2)}
              </td>

              <td className="px-4 py-3">
                {pooja.duration_minutes} min
              </td>

              <td className="px-4 py-3">
                {pooja.max_participants}
              </td>

              <td className="px-4 py-3">
                <Badge
                  variant={
                    pooja.online_booking
                      ? "default"
                      : "secondary"
                  }
                >
                  {pooja.online_booking
                    ? "Yes"
                    : "No"}
                </Badge>
              </td>

              <td className="px-4 py-3">
                <Badge
                  variant={
                    pooja.is_active
                      ? "default"
                      : "secondary"
                  }
                >
                  {pooja.is_active
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
                    <Link href={`/poojas/${pooja.id}`}>
                      <Eye className="h-4 w-4" />
                    </Link>
                  </Button>

                  <Button
                    variant="outline"
                    size="icon"
                    asChild
                  >
                    <Link
                      href={`/poojas/${pooja.id}/edit`}
                    >
                      <Pencil className="h-4 w-4" />
                    </Link>
                  </Button>

                  <DeleteConfirmationDialog
                    title="Delete Pooja"
                    description={`Delete "${pooja.name}"?`}
                    loading={
                      deleteMutation.isPending
                    }
                    onConfirm={() =>
                      handleDelete(pooja.id)
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