"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
import { usePoojas } from "@/features/poojas/hooks/usePoojas";

import {
  useCreateBooking,
  useUpdateBooking,
} from "../hooks/useBookings";

import type {
  Booking,
  CreateBookingRequest,
} from "../types/booking.types";

const schema = z.object({
  temple_id: z.string().min(1, "Temple is required"),

  pooja_id: z.string().min(1, "Pooja is required"),

  booking_date: z.string().min(1, "Booking date is required"),

  booking_time: z.string().min(1, "Booking time is required"),

  participants: z.coerce
    .number()
    .min(1, "Participants must be at least 1"),

  devotee_name: z
    .string()
    .min(2, "Devotee name is required"),

  devotee_mobile: z
    .string()
    .min(10, "Mobile number is required"),

  devotee_email: z
    .string()
    .email("Valid email is required"),

  special_notes: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

interface Props {
  booking?: Booking;
}

export default function BookingForm({
  booking,
}: Props) {
  const router = useRouter();

  const createMutation = useCreateBooking();

  const updateMutation = useUpdateBooking();

  const { data: temples = [] } =
    useTemples();

  const { data: poojas = [] } =
    usePoojas();

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
      temple_id: "",

      pooja_id: "",

      booking_date: "",

      booking_time: "",

      participants: 1,

      devotee_name: "",

      devotee_mobile: "",

      devotee_email: "",

      special_notes: "",
    },
  });

  useEffect(() => {
    if (!booking) return;

    reset({
      temple_id: booking.temple_id,

      pooja_id: booking.pooja_id,

      booking_date: booking.booking_date,

      booking_time: booking.booking_time,

      participants: booking.participants,

      devotee_name: booking.devotee_name,

      devotee_mobile: booking.devotee_mobile,

      devotee_email: booking.devotee_email,

      special_notes:
        booking.special_notes ?? "",
    });
  }, [booking, reset]);

  async function onSubmit(
    values: FormData
  ) {
    try {
      if (booking) {
        await updateMutation.mutateAsync({
          id: booking.id,
          data: values,
        });

        toast.success(
          "Booking updated successfully."
        );
      } else {
        await createMutation.mutateAsync(
          values as CreateBookingRequest
        );

        toast.success(
          "Booking created successfully."
        );
      }

      router.push("/bookings");

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
          {booking
            ? "Edit Booking"
            : "Create Booking"}
        </CardTitle>

      </CardHeader>

      <CardContent>

        <form
          onSubmit={handleSubmit(onSubmit)}
          className="space-y-6"
        >

          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                        {/* Temple */}
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
                disabled={!!booking}
              >
                <SelectTrigger id="temple">
                  <SelectValue placeholder="Select Temple" />
                </SelectTrigger>

                <SelectContent>
                  {temples.map((temple) => (
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

            {/* Pooja */}
            <div>
              <Label htmlFor="pooja">
                Pooja
              </Label>

              <Select
                value={watch("pooja_id")}
                onValueChange={(value) =>
                  setValue("pooja_id", value, {
                    shouldValidate: true,
                  })
                }
              >
                <SelectTrigger id="pooja">
                  <SelectValue placeholder="Select Pooja" />
                </SelectTrigger>

                <SelectContent>
                  {poojas
                    .filter(
                      (pooja) =>
                        pooja.temple_id ===
                        watch("temple_id")
                    )
                    .map((pooja) => (
                      <SelectItem
                        key={pooja.id}
                        value={pooja.id}
                      >
                        {pooja.name}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>

              {errors.pooja_id && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.pooja_id.message}
                </p>
              )}
            </div>

            {/* Booking Date */}
            <div>
              <Label htmlFor="booking_date">
                Booking Date
              </Label>

              <Input
                id="booking_date"
                type="date"
                {...register("booking_date")}
              />

              {errors.booking_date && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.booking_date.message}
                </p>
              )}
            </div>

            {/* Booking Time */}
            <div>
              <Label htmlFor="booking_time">
                Booking Time
              </Label>

              <Input
                id="booking_time"
                type="time"
                {...register("booking_time")}
              />

              {errors.booking_time && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.booking_time.message}
                </p>
              )}
            </div>

            {/* Participants */}
            <div>
              <Label htmlFor="participants">
                Participants
              </Label>

              <Input
                id="participants"
                type="number"
                min={1}
                {...register("participants")}
              />

              {errors.participants && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.participants.message}
                </p>
              )}
            </div>

            {/* Devotee Name */}
            <div>
              <Label htmlFor="devotee_name">
                Devotee Name
              </Label>

              <Input
                id="devotee_name"
                {...register("devotee_name")}
              />

              {errors.devotee_name && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.devotee_name.message}
                </p>
              )}
            </div>

            {/* Mobile */}
            <div>
              <Label htmlFor="devotee_mobile">
                Mobile
              </Label>

              <Input
                id="devotee_mobile"
                {...register("devotee_mobile")}
              />

              {errors.devotee_mobile && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.devotee_mobile.message}
                </p>
              )}
            </div>

            {/* Email */}
            <div>
              <Label htmlFor="devotee_email">
                Email
              </Label>

              <Input
                id="devotee_email"
                type="email"
                {...register("devotee_email")}
              />

              {errors.devotee_email && (
                <p className="mt-1 text-sm text-red-500">
                  {errors.devotee_email.message}
                </p>
              )}
            </div>

          </div>

          {/* Notes */}
          <div>
            <Label htmlFor="special_notes">
              Special Notes
            </Label>

            <Textarea
              id="special_notes"
              rows={4}
              {...register("special_notes")}
            />

            {errors.special_notes && (
              <p className="mt-1 text-sm text-red-500">
                {errors.special_notes.message}
              </p>
            )}
          </div>

          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={() =>
                router.push("/bookings")
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
              {booking
                ? "Update Booking"
                : "Create Booking"}
            </Button>
          </div>

        </form>

      </CardContent>
    </Card>
  );
}