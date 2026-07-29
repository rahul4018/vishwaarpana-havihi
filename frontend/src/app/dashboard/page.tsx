"use client";

import { useDashboardStats } from "@/features/dashboard/dashboard.hooks";

export default function DashboardPage() {
  const { data, isLoading, isError } = useDashboardStats();

  if (isLoading) {
    return (
      <div className="p-6">
        Loading dashboard...
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="p-6 text-red-600">
        Failed to load dashboard.
      </div>
    );
  }

  const stats = data.data;

  const cards = [
    {
      title: "Temples",
      value: stats.total_temples,
    },
    {
      title: "Priests",
      value: stats.total_priests,
    },
    {
      title: "Poojas",
      value: stats.total_poojas,
    },
    {
      title: "Bookings",
      value: stats.total_bookings,
    },
    {
      title: "Revenue",
      value: `₹${stats.total_revenue}`,
    },
  ];

  return (
    <div className="space-y-8 p-6">
      <div>
        <h1 className="text-3xl font-bold">
          Dashboard
        </h1>

        <p className="text-muted-foreground mt-2">
          Welcome to Vishwaarpana Havihi Admin Portal
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-5">
        {cards.map((card) => (
          <div
            key={card.title}
            className="rounded-xl border bg-white p-6 shadow-sm"
          >
            <p className="text-sm text-gray-500">
              {card.title}
            </p>

            <h2 className="mt-2 text-3xl font-bold">
              {card.value}
            </h2>
          </div>
        ))}
      </div>
    </div>
  );
}