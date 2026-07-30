"use client";

import { useParams } from "next/navigation";

import UserForm from "@/components/users/UserForm";
import { useUser } from "@/hooks/useUsers";

export default function EditUserPage() {
  const { id } = useParams();

  const {
    data,
    isLoading,
  } = useUser(id as string);

  if (isLoading) {
    return <div className="p-6">Loading...</div>;
  }

  if (!data) {
    return <div className="p-6">User not found.</div>;
  }

  return (
    <div className="mx-auto max-w-4xl p-6">
      <h1 className="mb-6 text-3xl font-bold">
        Edit User
      </h1>

      <div className="rounded-xl border bg-white p-8 shadow-sm">
        <UserForm
          mode="edit"
          userId={data.id}
          initialValues={{
            full_name: data.full_name,
            email: data.email,
            mobile: data.mobile ?? "",
            role_id: "",
            is_active: data.is_active,
            is_verified: data.is_verified,
          }}
        />
      </div>
    </div>
  );
}