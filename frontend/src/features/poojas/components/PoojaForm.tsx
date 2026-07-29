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
import { Checkbox } from "@/components/ui/checkbox";

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

import { useTemples } from "@/features/temples/hooks/useTemples";
import { useCategories } from "@/features/categories/hooks/useCategories";
import { usePriests } from "@/features/priests/hooks/usePriests";

import type { Temple } from "@/features/temples/types/temple.types";
import type { Category } from "@/features/categories/types/category.types";
import type { Priest } from "@/features/priests/types/priest.types";

import {
  useCreatePooja,
  useUpdatePooja,
} from "../hooks/usePoojas";

import type {
  CreatePoojaRequest,
  Pooja,
} from "../types/pooja.types";

const schema = z.object({
  temple_id: z.string().min(1, "Temple is required"),

  category_id: z.string().min(1, "Category is required"),

  priest_id: z.string().optional(),

  name: z.string().min(2, "Name is required"),

  slug: z.string().min(2, "Slug is required"),

  description: z.string().optional(),

  duration_minutes: z.coerce
    .number()
    .min(1, "Duration is required"),

  price: z.coerce
    .number()
    .min(0, "Price is required"),

  max_participants: z.coerce
    .number()
    .min(1, "Participants required"),

  online_booking: z.boolean(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  pooja?: Pooja;
}

export default function PoojaForm({
  pooja,
}: Props) {
  const router = useRouter();

  const createMutation = useCreatePooja();

  const updateMutation = useUpdatePooja();

  const { data: temples = [] } =
    useTemples();

  const { data: categories = [] } =
    useCategories();

  const { data: priests = [] } =
    usePriests();

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

      category_id: "",

      priest_id: "",

      name: "",

      slug: "",

      description: "",

      duration_minutes: 30,

      price: 0,

      max_participants: 1,

      online_booking: true,
    },
  });

  useEffect(() => {
    if (!pooja) return;

    reset({
      temple_id: pooja.temple_id,

      category_id: pooja.category_id,

      priest_id: pooja.priest_id ?? "",

      name: pooja.name,

      slug: pooja.slug,

      description: pooja.description ?? "",

      duration_minutes:
        pooja.duration_minutes,

      price: pooja.price,

      max_participants:
        pooja.max_participants,

      online_booking:
        pooja.online_booking,
    });
  }, [pooja, reset]);

  async function onSubmit(
    values: FormData
  ) {
    try {
      if (pooja) {
        await updateMutation.mutateAsync({
          id: pooja.id,

          data: {
            category_id:
              values.category_id,

            priest_id:
              values.priest_id || null,

            name: values.name,

            slug: values.slug,

            description:
              values.description,

            duration_minutes:
              values.duration_minutes,

            price: values.price,

            max_participants:
              values.max_participants,

            online_booking:
              values.online_booking,
          },
        });

        toast.success(
          "Pooja updated successfully"
        );
      } else {
        await createMutation.mutateAsync({
          temple_id: values.temple_id,

          category_id:
            values.category_id,

          priest_id:
            values.priest_id || null,

          name: values.name,

          slug: values.slug,

          description:
            values.description,

          duration_minutes:
            values.duration_minutes,

          price: values.price,

          max_participants:
            values.max_participants,

          online_booking:
            values.online_booking,
        } as CreatePoojaRequest);

        toast.success(
          "Pooja created successfully"
        );
      }

      router.push("/poojas");

      router.refresh();
    } catch {
      toast.error(
        "Something went wrong."
      );
    }
  }

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="space-y-6"
    >
              {/* Temple */}
      <div>
        <Label htmlFor="temple">Temple</Label>

        <Select
          value={watch("temple_id")}
          onValueChange={(value) =>
            setValue("temple_id", value, {
              shouldValidate: true,
            })
          }
          disabled={!!pooja}
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

      {/* Category */}
      <div>
        <Label htmlFor="category">
          Category
        </Label>

        <Select
          value={watch("category_id")}
          onValueChange={(value) =>
            setValue("category_id", value, {
              shouldValidate: true,
            })
          }
        >
          <SelectTrigger id="category">
            <SelectValue placeholder="Select category" />
          </SelectTrigger>

          <SelectContent>
            {categories
              .filter(
                (category: Category) =>
                  category.temple_id ===
                  watch("temple_id")
              )
              .map((category: Category) => (
                <SelectItem
                  key={category.id}
                  value={category.id}
                >
                  {category.name}
                </SelectItem>
              ))}
          </SelectContent>
        </Select>

        {errors.category_id && (
          <p className="mt-1 text-sm text-red-500">
            {errors.category_id.message}
          </p>
        )}
      </div>

      {/* Priest */}
      <div>
        <Label htmlFor="priest">
          Priest (Optional)
        </Label>

        <Select
          value={watch("priest_id")}
          onValueChange={(value) =>
            setValue("priest_id", value)
          }
        >
          <SelectTrigger id="priest">
            <SelectValue placeholder="Select priest" />
          </SelectTrigger>

          <SelectContent>
            <SelectItem value="">
              None
            </SelectItem>

            {priests
              .filter(
                (priest: Priest) =>
                  priest.temple_id ===
                  watch("temple_id")
              )
              .map((priest: Priest) => (
                <SelectItem
                  key={priest.id}
                  value={priest.id}
                >
                  {priest.full_name}
                </SelectItem>
              ))}
          </SelectContent>
        </Select>
      </div>

      {/* Name */}
      <div>
        <Label htmlFor="name">
          Name
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

      {/* Slug */}
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

      {/* Description */}
      <div>
        <Label htmlFor="description">
          Description
        </Label>

        <Textarea
          id="description"
          {...register("description")}
        />
      </div>

      {/* Duration */}
      <div>
        <Label htmlFor="duration">
          Duration (Minutes)
        </Label>

        <Input
          id="duration"
          type="number"
          {...register("duration_minutes")}
        />
      </div>

      {/* Price */}
      <div>
        <Label htmlFor="price">
          Price
        </Label>

        <Input
          id="price"
          type="number"
          {...register("price")}
        />
      </div>

      {/* Participants */}
      <div>
        <Label htmlFor="participants">
          Maximum Participants
        </Label>

        <Input
          id="participants"
          type="number"
          {...register("max_participants")}
        />
      </div>

      {/* Online Booking */}
      <div className="flex items-center space-x-2">
        <Checkbox
          id="online_booking"
          checked={watch("online_booking")}
          onCheckedChange={(checked) =>
            setValue(
              "online_booking",
              Boolean(checked)
            )
          }
        />

        <Label htmlFor="online_booking">
          Allow Online Booking
        </Label>
      </div>

      <Button
        type="submit"
        disabled={
          createMutation.isPending ||
          updateMutation.isPending
        }
      >
        {pooja
          ? "Update Pooja"
          : "Create Pooja"}
      </Button>
    </form>
  );
}