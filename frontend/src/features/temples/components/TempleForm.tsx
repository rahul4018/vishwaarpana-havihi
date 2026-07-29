"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import {
  templeSchema,
  TempleFormValues,
} from "../validation/temple.schema";

interface TempleFormProps {
  onSubmit: (values: TempleFormValues) => void;
  loading?: boolean;
  defaultValues?: Partial<TempleFormValues>;
}

export default function TempleForm({
  onSubmit,
  loading = false,
  defaultValues,
}: TempleFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<TempleFormValues>({
    resolver: zodResolver(templeSchema),
    defaultValues: {
      country: "India",
      ...defaultValues,
    },
  });

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-5"
    >
      <div>
        <label className="block mb-1">
          Temple Name
        </label>

        <input
          {...register("name")}
          className="w-full rounded border p-2"
        />

        <p className="text-sm text-red-500">
          {errors.name?.message}
        </p>
      </div>

      <div>
        <label className="block mb-1">
          Slug
        </label>

        <input
          {...register("slug")}
          className="w-full rounded border p-2"
        />

        <p className="text-sm text-red-500">
          {errors.slug?.message}
        </p>
      </div>

      <div>
        <label className="block mb-1">
          Address
        </label>

        <textarea
          {...register("address")}
          className="w-full rounded border p-2"
          rows={3}
        />

        <p className="text-sm text-red-500">
          {errors.address?.message}
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label>City</label>

          <input
            {...register("city")}
            className="w-full rounded border p-2"
          />
        </div>

        <div>
          <label>State</label>

          <input
            {...register("state")}
            className="w-full rounded border p-2"
          />
        </div>

        <div>
          <label>Country</label>

          <input
            {...register("country")}
            className="w-full rounded border p-2"
          />
        </div>
      </div>

      <div>
        <label>Email</label>

        <input
          {...register("email")}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label>Phone</label>

        <input
          {...register("phone")}
          className="w-full rounded border p-2"
        />
      </div>

      <div>
        <label>Website</label>

        <input
          {...register("website")}
          className="w-full rounded border p-2"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="rounded bg-orange-500 px-5 py-2 text-white"
      >
        {loading
          ? "Saving..."
          : "Save Temple"}
      </button>
    </form>
  );
}