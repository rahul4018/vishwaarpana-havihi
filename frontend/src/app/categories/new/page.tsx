import PageHeader from "@/components/shared/PageHeader";
import CategoryForm from "@/features/categories/components/CategoryForm";

export default function NewCategoryPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Create Category"
        description="Add a new pooja category"
      />

      <CategoryForm />
    </div>
  );
}