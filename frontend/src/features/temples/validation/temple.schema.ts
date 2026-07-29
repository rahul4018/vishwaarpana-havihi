import { z } from "zod";

export const templeSchema = z.object({
  name: z.string().min(2),
  slug: z.string().min(2),

  description: z.string().optional(),

  email: z
    .string()
    .email()
    .optional()
    .or(z.literal("")),

  phone: z.string().optional(),

  website: z.string().optional(),

  address: z.string().min(5),

  city: z.string().min(2),

  state: z.string().min(2),

  country: z.string().default("India"),

  postal_code: z.string().optional(),

  latitude: z.string().optional(),

  longitude: z.string().optional(),
});

export type TempleFormValues =
  z.infer<typeof templeSchema>;