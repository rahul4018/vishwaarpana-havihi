"use client";

import Link from "next/link";
import { useState } from "react";

import { useUsers } from "@/hooks/useUsers";

export default function UsersPage() {
  const { data = [], isLoading, error } = useUsers();

  const [search, setSearch] = useState("");

  const filteredUsers = data.filter((user) => {
    const keyword = search.toLowerCase();

    return (
      user.full_name.toLowerCase().includes(keyword) ||
      user.email.toLowerCase().includes(keyword) ||
      user.role.toLowerCase().includes(keyword)
    );
  });

  if (isLoading) {
    return (
      <div className="flex h-60 items-center justify-center">
        <p className="text-gray-500 text-lg">
          Loading users...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6">
        <h2 className="text-lg font-semibold text-red-600">
          Failed to load users
        </h2>

        <p className="mt-2 text-red-500">
          Please refresh the page and try again.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            User Management
          </h1>

          <p className="text-gray-500">
            Manage all platform users.
          </p>
        </div>

        <Link
          href="/users/new"
          className="rounded-lg bg-blue-600 px-5 py-2.5 font-medium text-white transition hover:bg-blue-700"
        >
          + Add User
        </Link>
      </div>

      {/* Search */}
      <div>
        <input
          type="text"
          placeholder="Search users..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full rounded-lg border px-4 py-2 outline-none focus:border-blue-500"
        />
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-xl border bg-white shadow-sm">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-5 py-3 text-left font-semibold">
                Name
              </th>

              <th className="px-5 py-3 text-left font-semibold">
                Email
              </th>

              <th className="px-5 py-3 text-left font-semibold">
                Role
              </th>

              <th className="px-5 py-3 text-left font-semibold">
                Status
              </th>

              <th className="px-5 py-3 text-center font-semibold">
                Actions
              </th>
            </tr>
          </thead>

          <tbody>
            {filteredUsers.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="py-12 text-center text-gray-500"
                >
                  No users found.
                </td>
              </tr>
            ) : (
              filteredUsers.map((user) => (
                <tr
                  key={user.id}
                  className="border-t transition hover:bg-gray-50"
                >
                  <td className="px-5 py-4 font-medium">
                    {user.full_name}
                  </td>

                  <td className="px-5 py-4">
                    {user.email}
                  </td>

                  <td className="px-5 py-4">
                    <span className="rounded-full bg-blue-100 px-3 py-1 text-sm font-medium text-blue-700">
                      {user.role}
                    </span>
                  </td>

                  <td className="px-5 py-4">
                    {user.is_active ? (
                      <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
                        Active
                      </span>
                    ) : (
                      <span className="rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-700">
                        Inactive
                      </span>
                    )}
                  </td>

                  <td className="px-5 py-4">
                    <div className="flex justify-center gap-2">
                      <Link
                        href={`/users/${user.id}`}
                        className="rounded-md border px-3 py-1 text-sm transition hover:bg-gray-100"
                      >
                        View
                      </Link>

                      <Link
                        href={`/users/${user.id}/edit`}
                        className="rounded-md bg-yellow-500 px-3 py-1 text-sm text-white transition hover:bg-yellow-600"
                      >
                        Edit
                      </Link>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Footer */}
      <div className="text-sm text-gray-500">
        Total Users:{" "}
        <span className="font-semibold">
          {filteredUsers.length}
        </span>
      </div>
    </div>
  );
}