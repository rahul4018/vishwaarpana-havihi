"use client";

import { Bell, Menu, User } from "lucide-react";

export default function TopNavbar() {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-white px-6">
      <div className="flex items-center gap-3">
        <button className="rounded-md p-2 hover:bg-gray-100">
          <Menu className="h-5 w-5" />
        </button>

        <h1 className="text-lg font-semibold">
          Vishwaarpana Havihi
        </h1>
      </div>

      <div className="flex items-center gap-4">
        <button className="rounded-full p-2 hover:bg-gray-100">
          <Bell className="h-5 w-5" />
        </button>

        <button className="flex items-center gap-2 rounded-lg border px-3 py-2 hover:bg-gray-50">
          <User className="h-5 w-5" />
          <span>Admin</span>
        </button>
      </div>
    </header>
  );
}