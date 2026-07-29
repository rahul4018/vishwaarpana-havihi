"use client";

interface EmptyStateProps {
  title: string;
  description?: string;
}

export default function EmptyState({
  title,
  description,
}: EmptyStateProps) {
  return (
    <div className="rounded-xl border border-dashed p-10 text-center">
      <h2 className="text-xl font-semibold">
        {title}
      </h2>

      {description && (
        <p className="mt-2 text-gray-500">
          {description}
        </p>
      )}
    </div>
  );
}