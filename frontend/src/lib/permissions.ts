export type UserRole =
  | "SUPER_ADMIN"
  | "ADMIN"
  | "TEMPLE_ADMIN"
  | "PRIEST"
  | "DEVOTEE";

export const permissions: Record<UserRole, string[]> = {
  SUPER_ADMIN: ["*"],

  ADMIN: [
    "/dashboard",
    "/temples",
    "/priests",
    "/categories",
    "/poojas",
    "/bookings",
    "/payments",
    "/invoices",
    "/gallery",
    "/notifications",
    "/reviews",
    "/contacts",
  ],

  TEMPLE_ADMIN: [
    "/dashboard",
    "/bookings",
    "/priests",
    "/poojas",
    "/gallery",
  ],

  PRIEST: [
    "/dashboard",
    "/bookings",
    "/availability",
    "/profile",
  ],

  DEVOTEE: [
    "/dashboard",
    "/bookings",
    "/profile",
  ],
};

export function hasPermission(
  role: UserRole,
  path: string
): boolean {
  const allowed = permissions[role];

  if (!allowed) return false;

  if (allowed.includes("*")) return true;

  return allowed.some((route) => path.startsWith(route));
}