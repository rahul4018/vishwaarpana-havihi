"use client";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onChange: (page: number) => void;
}

export default function Pagination({
  currentPage,
  totalPages,
  onChange,
}: PaginationProps) {
  if (totalPages <= 1) return null;

  return (
    <div className="flex justify-end gap-2">
      <button
        onClick={() => onChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="rounded border px-4 py-2 disabled:opacity-50"
      >
        Previous
      </button>

      <span className="flex items-center px-2">
        {currentPage} / {totalPages}
      </span>

      <button
        onClick={() => onChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="rounded border px-4 py-2 disabled:opacity-50"
      >
        Next
      </button>
    </div>
  );
}