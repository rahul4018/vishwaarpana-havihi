"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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

import { usePriests } from "@/features/priests/hooks/usePriests";

import {
  useCreatePriestAvailability,
  useUpdatePriestAvailability,
} from "../hooks/usePriestAvailability";

import type {
  CreatePriestAvailabilityRequest,
  PriestAvailability,
} from "../types/priestAvailability.types";

const schema = z.object({
  priest_id: z.string().min(
    1,
    "Priest is required"
  ),

  available_date: z.string().min(
    1,
    "Available date is required"
  ),

  start_time: z.string().min(
    1,
    "Start time is required"
  ),

  end_time: z.string().min(
    1,
    "End time is required"
  ),

  is_available: z.boolean(),

  remarks: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  availability?: PriestAvailability;
}

export default function AvailabilityForm({
  availability,
}: Props) {
  const router = useRouter();

  const createMutation =
    useCreatePriestAvailability();

  const updateMutation =
    useUpdatePriestAvailability();

  const { data: priests = [] } =
    usePriests();

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors },
  } = useForm<FormData>({
    resolver: zodResolver(schema),

    defaultValues: {
      priest_id: "",

      available_date: "",

      start_time: "",

      end_time: "",

      is_available: true,

      remarks: "",
    },
  });

  useEffect(() => {
    if (!availability) return;

    reset({
      priest_id:
        availability.priest_id,

      available_date:
        availability.available_date,

      start_time:
        availability.start_time,

      end_time:
        availability.end_time,

      is_available:
        availability.is_available,

      remarks:
        availability.remarks ?? "",
    });
  }, [availability, reset]);
    async function onSubmit(
    values: FormData
  ) {
    try {
      if (availability) {
        await updateMutation.mutateAsync({
          id: availability.id,
          data: values,
        });

        toast.success(
          "Availability updated successfully."
        );
      } else {
        await createMutation.mutateAsync(
          values as CreatePriestAvailabilityRequest
        );

        toast.success(
          "Availability created successfully."
        );
      }

      router.push(
        "/priest-availability"
      );

      router.refresh();
    } catch {
      toast.error(
        "Something went wrong."
      );
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          {availability
            ? "Edit Priest Availability"
            : "Create Priest Availability"}
        </CardTitle>
      </CardHeader>

      <CardContent>
        <form
          onSubmit={handleSubmit(
            onSubmit
          )}
          className="space-y-6"
        >
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">

            {/* Priest */}
            <div>
              <Label htmlFor="priest">
                Priest
              </Label>

              <Select
                value={watch("priest_id")}
                onValueChange={(value) =>
                  setValue(
                    "priest_id",
                    value,
                    {
                      shouldValidate: true,
                    }
                  )
                }
              >
                <SelectTrigger id="priest">
                  <SelectValue placeholder="Select Priest" />
                </SelectTrigger>

                <SelectContent>
                  {priests.map(
                    (priest) => (
                      <SelectItem
                        key={priest.id}
                        value={priest.id}
                      >
                        {priest.full_name}
                      </SelectItem>
                    )
                  )}
                </SelectContent>
              </Select>

              {errors.priest_id && (
                <p className="mt-1 text-sm text-red-500">
                  {
                    errors.priest_id
                      .message
                  }
                </p>
              )}
            </div>

            {/* Available Date */}
            <div>
              <Label htmlFor="available_date">
                Available Date
              </Label>

              <Input
                id="available_date"
                type="date"
                {...register(
                  "available_date"
                )}
              />

              {errors.available_date && (
                <p className="mt-1 text-sm text-red-500">
                  {
                    errors
                      .available_date
                      .message
                  }
                </p>
              )}
            </div>

            {/* Start Time */}
            <div>
              <Label htmlFor="start_time">
                Start Time
              </Label>

              <Input
                id="start_time"
                type="time"
                {...register(
                  "start_time"
                )}
              />

              {errors.start_time && (
                <p className="mt-1 text-sm text-red-500">
                  {
                    errors
                      .start_time
                      .message
                  }
                </p>
              )}
            </div>

            {/* End Time */}
            <div>
              <Label htmlFor="end_time">
                End Time
              </Label>

              <Input
                id="end_time"
                type="time"
                {...register(
                  "end_time"
                )}
              />

              {errors.end_time && (
                <p className="mt-1 text-sm text-red-500">
                  {
                    errors
                      .end_time
                      .message
                  }
                </p>
              )}
            </div>
                        {/* Availability Status */}
            <div>
              <Label>
                Availability Status
              </Label>

              <Select
                value={
                  watch("is_available")
                    ? "true"
                    : "false"
                }
                onValueChange={(value) =>
                  setValue(
                    "is_available",
                    value === "true"
                  )
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>

                <SelectContent>
                  <SelectItem value="true">
                    Available
                  </SelectItem>

                  <SelectItem value="false">
                    Unavailable
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Remarks */}
            <div className="md:col-span-2">
              <Label htmlFor="remarks">
                Remarks
              </Label>

              <Textarea
                id="remarks"
                rows={4}
                placeholder="Enter remarks (optional)"
                {...register("remarks")}
              />

              {errors.remarks && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.remarks.message}
                </p>
              )}
            </div>

          </div>

          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={() =>
                router.push(
                  "/priest-availability"
                )
              }
            >
              Cancel
            </Button>

            <Button
              type="submit"
              disabled={
                createMutation.isPending ||
                updateMutation.isPending
              }
            >
              {availability
                ? "Update Availability"
                : "Create Availability"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}