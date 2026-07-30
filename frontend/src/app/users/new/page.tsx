"use client";

import Link from "next/link";

import UserForm from "@/components/users/UserForm";

export default function NewUserPage() {
  return (
    <div className="mx-auto max-w-4xl p-6">
      {/* Header */}
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">
            Create User
          </h1>

          <p className="mt-1 text-gray-500">
            Create a new user account and assign a role.
          </p>
        </div>

        <Link
          href="/users"
          className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium transition hover:bg-gray-100"
        >
          ← Back
        </Link>
      </div>

      {/* Form Card */}
      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <UserForm />
      </div>
    </div>
  );
}