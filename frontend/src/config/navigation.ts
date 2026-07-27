import type { NavigationItem } from "@/types/navigation";

export const navigation: NavigationItem[] = [
  {
    id: "dashboard",
    title: "Dashboard",
    href: "/dashboard",
    roles: ["admin", "owner", "priest", "catering", "customer"],
  },

  {
    id: "temple",
    title: "Temple",
    roles: ["admin", "owner"],
    sections: [
      {
        title: "Temple Management",
        children: [
          {
            id: "temple-information",
            title: "Temple Information",
            description: "Manage temple information",
            href: "/dashboard/temple",
            roles: ["admin", "owner"],
          },
          {
            id: "gallery",
            title: "Gallery",
            description: "Temple photos and media",
            href: "/dashboard/gallery",
            roles: ["admin", "owner"],
          },
          {
            id: "timings",
            title: "Temple Timings",
            description: "Opening and closing schedules",
            href: "/dashboard/timings",
            roles: ["admin", "owner"],
          },
        ],
      },
      {
        title: "Priest Management",
        children: [
          {
            id: "priests",
            title: "Priests",
            description: "Manage priests",
            href: "/dashboard/priests",
            roles: ["admin", "owner"],
          },
          {
            id: "attendance",
            title: "Attendance",
            description: "Track attendance",
            href: "/dashboard/attendance",
            roles: ["admin", "owner", "priest"],
          },
          {
            id: "schedule",
            title: "Schedules",
            description: "Daily priest schedules",
            href: "/dashboard/schedules",
            roles: ["admin", "owner", "priest"],
          },
        ],
      },
      {
        title: "Services",
        children: [
          {
            id: "poojas",
            title: "Poojas",
            description: "Temple pooja services",
            href: "/dashboard/poojas",
            roles: ["admin", "owner"],
          },
          {
            id: "festivals",
            title: "Festivals",
            description: "Festival management",
            href: "/dashboard/festivals",
            roles: ["admin", "owner"],
          },
          {
            id: "donations",
            title: "Donations",
            description: "Temple donations",
            href: "/dashboard/donations",
            roles: ["admin", "owner"],
          },
        ],
      },
    ],
  },

  {
    id: "bookings",
    title: "Bookings",
    roles: ["admin", "owner", "customer"],
    sections: [
      {
        title: "Booking Management",
        children: [
          {
            id: "new-booking",
            title: "New Booking",
            description: "Create a booking",
            href: "/dashboard/bookings/new",
            roles: ["admin", "owner", "customer"],
          },
          {
            id: "booking-list",
            title: "Booking List",
            description: "View all bookings",
            href: "/dashboard/bookings",
            roles: ["admin", "owner"],
          },
          {
            id: "calendar",
            title: "Calendar",
            description: "Booking calendar",
            href: "/dashboard/bookings/calendar",
            roles: ["admin", "owner"],
          },
          {
            id: "my-bookings",
            title: "My Bookings",
            description: "Customer bookings",
            href: "/dashboard/my-bookings",
            roles: ["customer"],
          },
        ],
      },
    ],
  },

  {
    id: "finance",
    title: "Finance",
    roles: ["admin", "owner"],
    sections: [
      {
        title: "Finance",
        children: [
          {
            id: "payments",
            title: "Payments",
            description: "Manage payments",
            href: "/dashboard/payments",
            roles: ["admin", "owner"],
          },
          {
            id: "invoices",
            title: "Invoices",
            description: "Generate invoices",
            href: "/dashboard/invoices",
            roles: ["admin", "owner"],
          },
          {
            id: "expenses",
            title: "Expenses",
            description: "Temple expenses",
            href: "/dashboard/expenses",
            roles: ["admin", "owner"],
          },
        ],
      },
    ],
  },

  {
    id: "inventory",
    title: "Inventory",
    roles: ["admin", "owner", "catering"],
    sections: [
      {
        title: "Inventory",
        children: [
          {
            id: "stock",
            title: "Stock",
            description: "Inventory stock",
            href: "/dashboard/inventory",
            roles: ["admin", "owner", "catering"],
          },
          {
            id: "suppliers",
            title: "Suppliers",
            description: "Supplier management",
            href: "/dashboard/suppliers",
            roles: ["admin", "owner"],
          },
          {
            id: "purchases",
            title: "Purchases",
            description: "Purchase history",
            href: "/dashboard/purchases",
            roles: ["admin", "owner"],
          },
        ],
      },
    ],
  },

  {
    id: "reports",
    title: "Reports",
    roles: ["admin", "owner"],
    sections: [
      {
        title: "Analytics",
        children: [
          {
            id: "daily-report",
            title: "Daily Report",
            description: "Daily analytics",
            href: "/dashboard/reports/daily",
            roles: ["admin", "owner"],
          },
          {
            id: "monthly-report",
            title: "Monthly Report",
            description: "Monthly analytics",
            href: "/dashboard/reports/monthly",
            roles: ["admin", "owner"],
          },
          {
            id: "financial-report",
            title: "Financial Report",
            description: "Finance analytics",
            href: "/dashboard/reports/finance",
            roles: ["admin", "owner"],
          },
        ],
      },
    ],
  },

  {
    id: "settings",
    title: "Settings",
    roles: ["admin", "owner"],
    sections: [
      {
        title: "Administration",
        children: [
          {
            id: "users",
            title: "Users",
            description: "Manage users",
            href: "/dashboard/users",
            roles: ["admin"],
          },
          {
            id: "roles",
            title: "Roles & Permissions",
            description: "Access control",
            href: "/dashboard/roles",
            roles: ["admin"],
          },
          {
            id: "preferences",
            title: "Preferences",
            description: "Application settings",
            href: "/dashboard/preferences",
            roles: ["admin", "owner"],
          },
        ],
      },
    ],
  },
];