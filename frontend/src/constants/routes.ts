/**
 * Application Routes
 */

export const ROUTES = {
  HOME: "/",

  AUTH: {
    LOGIN: "/login",
    REGISTER: "/register",
    FORGOT_PASSWORD: "/forgot-password",
    RESET_PASSWORD: "/reset-password",
  },

  DASHBOARD: "/dashboard",

  TEMPLE: "/temples",

  CATEGORY: "/categories",

  PRIEST: "/priests",

  POOJA: "/poojas",

  BOOKINGS: "/bookings",

  PAYMENTS: "/payments",

  INVOICES: "/invoices",

  GALLERY: "/gallery",

  CONTACTS: "/contacts",

  NOTIFICATIONS: "/notifications",

  REVIEWS: "/reviews",

  SETTINGS: "/settings",

  PROFILE: "/profile",
} as const;