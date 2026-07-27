import {
  LayoutDashboard,
  Users,
  Building2,
  CalendarCheck,
  Flame,
  BarChart3,
  Settings,
} from "lucide-react";

import type { NavigationItem } from "@/types/navigation";

export const dashboardMenu: NavigationItem[] = [
  {
    title: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    title: "Users",
    href: "/dashboard/users",
    icon: Users,
  },
  {
    title: "Temples",
    href: "/dashboard/temples",
    icon: Building2,
  },
  {
    title: "Bookings",
    href: "/dashboard/bookings",
    icon: CalendarCheck,
  },
  {
    title: "Poojas",
    href: "/dashboard/poojas",
    icon: Flame,
  },
  {
    title: "Reports",
    href: "/dashboard/reports",
    icon: BarChart3,
  },
  {
    title: "Settings",
    href: "/dashboard/settings",
    icon: Settings,
  },
];