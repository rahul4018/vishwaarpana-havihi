"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { useTemples } from "@/features/temples/hooks/useTemples";
import type { Temple } from "@/features/temples/types/temple.types";

import {
  useCreateCategory,
  useUpdateCategory,
} from "../hooks/useCategories";

import type {
  Category,
  CreateCategoryRequest,
} from "../types/category.types";

const schema = z.object({
  temple_id: z.string().min(1, "Temple is required"),
  name: z.string().min(2, "Name is required"),
  slug: z.string().min(2, "Slug is required"),
  description: z.string().optional(),
  display_order: z.coerce.number().min(1),
});

type FormData = z.infer<typeof schema>;

interface Props {
  category?: Category;
}

export default function CategoryForm({
  category,
}: Props) {
  const router = useRouter();

  const createMutation = useCreateCategory();
  const updateMutation = useUpdateCategory();

  const { data: temples = [] } = useTemples();

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    reset,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      temple_id: "",
      name: "",
      slug: "",
      description: "",
      display_order: 1,
    },
  });

  useEffect(() => {
    if (category) {
      reset({
        temple_id: category.temple_id,
        name: category.name,
        slug: category.slug,
        description: category.description ?? "",
        display_order: category.display_order,
      });
    }
  }, [category, reset]);

  async function onSubmit(values: FormData) {
    try {
      if (category) {
        await updateMutation.mutateAsync({
          id: category.id,
          data: values,
        });

        toast.success(
          "Category updated successfully"
        );
      } else {
        await createMutation.mutateAsync(
          values as CreateCategoryRequest
        );

        toast.success(
          "Category created successfully"
        );
      }

      router.push("/categories");
      router.refresh();
    } catch {
      toast.error("Something went wrong");
    }
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-6"
    >
      <div>
        <Label htmlFor="temple">
          Temple
        </Label>

        <Select
          value={watch("temple_id")}
          onValueChange={(value) =>
            setValue("temple_id", value, {
              shouldValidate: true,
            })
          }
        >
          <SelectTrigger id="temple">
            <SelectValue placeholder="Select temple" />
          </SelectTrigger>

          <SelectContent>
            {temples.map((temple: Temple) => (
              <SelectItem
                key={temple.id}
                value={temple.id}
              >
                {temple.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {errors.temple_id && (
          <p className="mt-1 text-sm text-red-500">
            {errors.temple_id.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="name">
          Category Name
        </Label>

        <Input
          id="name"
          {...register("name")}
        />

        {errors.name && (
          <p className="mt-1 text-sm text-red-500">
            {errors.name.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="slug">
          Slug
        </Label>

        <Input
          id="slug"
          {...register("slug")}
        />

        {errors.slug && (
          <p className="mt-1 text-sm text-red-500">
            {errors.slug.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="display_order">
          Display Order
        </Label>

        <Input
          id="display_order"
          type="number"
          {...register("display_order")}
        />

        {errors.display_order && (
          <p className="mt-1 text-sm text-red-500">
            {errors.display_order.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="description">
          Description
        </Label>

        <Textarea
          id="description"
          {...register("description")}
        />
      </div>

      <Button
        type="submit"
        disabled={
          createMutation.isPending ||
          updateMutation.isPending
        }
      >
        {category
          ? "Update Category"
          : "Create Category"}
      </Button>
    </form>
  );
}