"use client";

import Link from "next/link";

import PageHeader from "@/components/shared/PageHeader";
import { Button } from "@/components/ui/button";

import CategoryTable from "@/features/categories/components/CategoryTable";
import { useCategories } from "@/features/categories/hooks/useCategories";

export default function CategoriesPage() {
  const {
    data: categories = [],
    isLoading,
    isError,
  } = useCategories();

  if (isLoading) {
    return (
      <div className="p-6">
        Loading categories...
      </div>
    );
  }

  if (isError) {
    return (
      <div className="p-6 text-red-500">
        Failed to load categories.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Categories"
        description="Manage pooja categories"
        action={
          <Button asChild>
            <Link href="/categories/new">
              Add Category
            </Link>
          </Button>
        }
      />

      <CategoryTable
        categories={categories}
      />
    </div>
  );
}