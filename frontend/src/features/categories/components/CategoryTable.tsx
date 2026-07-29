"use client";

import Link from "next/link";
import { Eye, Pencil, Trash2 } from "lucide-react";
import { toast } from "sonner";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import DeleteConfirmationDialog from "@/components/shared/DeleteConfirmationDialog";

import { useDeleteCategory } from "../hooks/useCategories";
import { Category } from "../types/category.types";

interface CategoryTableProps {
  categories: Category[];
}

export default function CategoryTable({
  categories,
}: CategoryTableProps) {
  const deleteMutation = useDeleteCategory();

  async function handleDelete(id: string) {
    try {
      await deleteMutation.mutateAsync(id);
      toast.success("Category deleted successfully");
    } catch {
      toast.error("Failed to delete category");
    }
  }

  if (categories.length === 0) {
    return (
      <div className="rounded-lg border bg-card p-10 text-center text-muted-foreground">
        No categories found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-lg border bg-background">
      <table className="w-full">
        <thead className="border-b bg-muted/50">
          <tr>
            <th className="px-4 py-3 text-left">
              Name
            </th>

            <th className="px-4 py-3 text-left">
              Slug
            </th>

            <th className="px-4 py-3 text-left">
              Order
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
          {categories.map((category) => (
            <tr
              key={category.id}
              className="border-b last:border-none"
            >
              <td className="px-4 py-3 font-medium">
                {category.name}
              </td>

              <td className="px-4 py-3">
                {category.slug}
              </td>

              <td className="px-4 py-3">
                {category.display_order}
              </td>

              <td className="px-4 py-3">
                <Badge
                  variant={
                    category.is_active
                      ? "default"
                      : "secondary"
                  }
                >
                  {category.is_active
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
                    <Link
                      href={`/categories/${category.id}`}
                    >
                      <Eye className="h-4 w-4" />
                    </Link>
                  </Button>

                  <Button
                    variant="outline"
                    size="icon"
                    asChild
                  >
                    <Link
                      href={`/categories/${category.id}/edit`}
                    >
                      <Pencil className="h-4 w-4" />
                    </Link>
                  </Button>

                  <DeleteConfirmationDialog
                    title="Delete Category"
                    description={`Delete "${category.name}"?`}
                    loading={
                      deleteMutation.isPending
                    }
                    onConfirm={() =>
                      handleDelete(category.id)
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