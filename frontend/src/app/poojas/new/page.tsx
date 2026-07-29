import PageHeader from "@/components/shared/PageHeader";
import PoojaForm from "@/features/poojas/components/PoojaForm";

export default function NewPoojaPage() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Create Pooja"
        description="Add a new pooja"
      />

      <PoojaForm />
    </div>
  );
}