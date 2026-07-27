/**
 * API Endpoints
 */

export const API = {
  AUTH: {
    LOGIN: "/auth/login",
    REFRESH: "/auth/refresh",
    LOGOUT: "/auth/logout",
    ME: "/auth/me",
  },

  TEMPLES: "/temples",

  CATEGORIES: "/categories",

  PRIESTS: "/priests",

  POOJAS: "/poojas",

  BOOKINGS: "/bookings",

  PAYMENTS: "/payments",

  GALLERY: "/gallery",

  CONTACTS: "/contacts",

  REVIEWS: "/reviews",

  NOTIFICATIONS: "/notifications",

  INVOICES: "/invoices",

  KUNDLI: "/kundli",

  CHAT: "/chat",
} as const;