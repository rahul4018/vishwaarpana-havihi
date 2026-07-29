"use client";

import { useParams } from "next/navigation";

import PageHeader from "@/components/shared/PageHeader";

import CategoryForm from "@/features/categories/components/CategoryForm";
import { useCategory } from "@/features/categories/hooks/useCategories";

export default function EditCategoryPage() {
  const params = useParams();

  const { data, isLoading, isError } = useCategory(
    params.id as string
  );

  if (isLoading) {
    return <div className="p-6">Loading...</div>;
  }

  if (isError || !data) {
    return (
      <div className="p-6 text-red-500">
        Category not found.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader
        title="Edit Category"
        description="Update category details"
      />

      <CategoryForm category={data} />
    </div>
  );
}