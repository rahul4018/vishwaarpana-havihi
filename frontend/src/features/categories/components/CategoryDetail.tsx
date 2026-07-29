"use client";

import { Badge } from "@/components/ui/badge";

import type { Category } from "../types/category.types";

interface Props {
  category: Category;
}

export default function CategoryDetail({
  category,
}: Props) {
  return (
    <div className="rounded-lg border bg-card p-6 space-y-4">
      <div>
        <h2 className="text-2xl font-bold">
          {category.name}
        </h2>

        <p className="text-muted-foreground">
          {category.slug}
        </p>
      </div>

      <div>
        <strong>Description:</strong>
        <p>{category.description || "-"}</p>
      </div>

      <div>
        <strong>Display Order:</strong>{" "}
        {category.display_order}
      </div>

      <div>
        <strong>Status:</strong>{" "}
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
      </div>
    </div>
  );
}