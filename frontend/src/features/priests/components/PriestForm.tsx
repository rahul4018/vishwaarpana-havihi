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

import {
  useCreatePriest,
  useUpdatePriest,
} from "../hooks/usePriests";

import type {
  CreatePriestRequest,
  Priest,
} from "../types/priest.types";

import { useTemples } from "@/features/temples/hooks/useTemples";
import type { Temple } from "@/features/temples/types/temple.types";

const schema = z.object({
  temple_id: z.string().min(1, "Temple is required"),
  full_name: z.string().min(3, "Name is required"),
  email: z.string().email().optional().or(z.literal("")),
  phone: z.string().min(10, "Phone is required"),
  experience_years: z.coerce.number().min(0),
  specialization: z.string().optional(),
  bio: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  priest?: Priest;
}

export default function PriestForm({ priest }: Props) {
  const router = useRouter();

  const createMutation = useCreatePriest();
  const updateMutation = useUpdatePriest();

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
      full_name: "",
      email: "",
      phone: "",
      experience_years: 0,
      specialization: "",
      bio: "",
    },
  });

  useEffect(() => {
    if (priest) {
      reset({
        temple_id: priest.temple_id,
        full_name: priest.full_name,
        email: priest.email ?? "",
        phone: priest.phone,
        experience_years: priest.experience_years,
        specialization: priest.specialization ?? "",
        bio: priest.bio ?? "",
      });
    }
  }, [priest, reset]);

  async function onSubmit(values: FormData) {
    try {
      if (priest) {
        await updateMutation.mutateAsync({
          id: priest.id,
          data: values,
        });

        toast.success("Priest updated successfully");
      } else {
        await createMutation.mutateAsync(
          values as CreatePriestRequest
        );

        toast.success("Priest created successfully");
      }

      router.push("/priests");
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
        <Label htmlFor="temple">Temple</Label>

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
        <Label htmlFor="full_name">Full Name</Label>
        <Input
          id="full_name"
          {...register("full_name")}
        />
        {errors.full_name && (
          <p className="mt-1 text-sm text-red-500">
            {errors.full_name.message}
          </p>
        )}
      </div>

      <div>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          {...register("email")}
        />
      </div>

      <div>
        <Label htmlFor="phone">Phone</Label>
        <Input
          id="phone"
          {...register("phone")}
        />
      </div>

      <div>
        <Label htmlFor="experience_years">
          Experience (Years)
        </Label>
        <Input
          id="experience_years"
          type="number"
          {...register("experience_years")}
        />
      </div>

      <div>
        <Label htmlFor="specialization">
          Specialization
        </Label>
        <Input
          id="specialization"
          {...register("specialization")}
        />
      </div>

      <div>
        <Label htmlFor="bio">Bio</Label>
        <Textarea
          id="bio"
          {...register("bio")}
        />
      </div>

      <Button
        type="submit"
        disabled={
          createMutation.isPending ||
          updateMutation.isPending
        }
      >
        {priest
          ? "Update Priest"
          : "Create Priest"}
      </Button>
    </form>
  );
}