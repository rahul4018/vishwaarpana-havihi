"use client";

import { ReactNode } from "react";

interface DataTableColumn<T> {
  key: keyof T | string;
  title: string;
  render?: (row: T) => ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: DataTableColumn<T>[];
  data: T[];
  emptyMessage?: string;
}

export default function DataTable<T extends { id: string }>({
  columns,
  data,
  emptyMessage = "No records found.",
}: DataTableProps<T>) {
  return (
    <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
      <table className="min-w-full">
        <thead className="border-b bg-gray-100">
          <tr>
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className={`p-4 text-left font-semibold ${column.className ?? ""}`}
              >
                {column.title}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.length > 0 ? (
            data.map((row) => (
              <tr
                key={row.id}
                className="border-b transition hover:bg-gray-50"
              >
                {columns.map((column) => (
                  <td
                    key={String(column.key)}
                    className={`p-4 ${column.className ?? ""}`}
                  >
                    {column.render
                      ? column.render(row)
                      : String(
                          row[column.key as keyof T] ?? "-"
                        )}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length}
                className="p-10 text-center text-gray-500"
              >
                {emptyMessage}
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}