"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";

import { useRoles } from "@/hooks/useRoles";
import { useCreateUser } from "@/hooks/useUsers";

export default function UserForm() {
  const router = useRouter();

  const { data: roles = [], isLoading: loadingRoles } = useRoles();
  const createUser = useCreateUser();

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    mobile: "",
    password: "",
    role_id: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    try {
      await createUser.mutateAsync(form);

      toast.success("User created successfully");

      router.push("/users");
      router.refresh();
    } catch (error) {
      console.error(error);
      toast.error("Failed to create user");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="mb-2 block text-sm font-medium">
          Full Name
        </label>
        <input
          type="text"
          name="full_name"
          value={form.full_name}
          onChange={handleChange}
          className="w-full rounded-lg border px-3 py-2"
          required
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium">
          Email
        </label>
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          className="w-full rounded-lg border px-3 py-2"
          required
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium">
          Mobile
        </label>
        <input
          type="text"
          name="mobile"
          value={form.mobile}
          onChange={handleChange}
          className="w-full rounded-lg border px-3 py-2"
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium">
          Password
        </label>
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          className="w-full rounded-lg border px-3 py-2"
          required
        />
      </div>

      <div>
        <label className="mb-2 block text-sm font-medium">
          Role
        </label>

        <select
          name="role_id"
          value={form.role_id}
          onChange={handleChange}
          className="w-full rounded-lg border px-3 py-2"
          required
        >
          <option value="">Select Role</option>

          {loadingRoles ? (
            <option>Loading...</option>
          ) : (
            roles.map((role) => (
              <option key={role.id} value={role.id}>
                {role.name}
              </option>
            ))
          )}
        </select>
      </div>

      <button
        type="submit"
        disabled={createUser.isPending}
        className="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
      >
        {createUser.isPending ? "Creating..." : "Create User"}
      </button>
    </form>
  );
}