"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Landmark,
  UserCog,
  FolderTree,
  ScrollText,
  CalendarDays,
  CreditCard,
  Users,
  Images,
  Settings,
} from "lucide-react";

const menus = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Temples",
    href: "/temples",
    icon: Landmark,
  },
  {
    name: "Priests",
    href: "/priests",
    icon: UserCog,
  },
  {
    name: "Categories",
    href: "/categories",
    icon: FolderTree,
  },
  {
    name: "Poojas",
    href: "/poojas",
    icon: ScrollText,
  },
  {
    name: "Bookings",
    href: "/bookings",
    icon: CalendarDays,
  },
  {
    name: "Payments",
    href: "/payments",
    icon: CreditCard,
  },
  {
    name: "Users",
    href: "/users",
    icon: Users,
  },
  {
    name: "Gallery",
    href: "/gallery",
    icon: Images,
  },
  {
    name: "Settings",
    href: "/settings",
    icon: Settings,
  },
];

export default function AppSidebar() {
  const pathname = usePathname();

  return (
    <aside className="sticky top-0 flex h-screen w-64 flex-col border-r bg-white">
      <div className="border-b px-6 py-6">
        <h1 className="text-xl font-bold">
          Vishwaarpana
        </h1>

        <p className="text-sm text-gray-500">
          Admin Panel
        </p>
      </div>

      <nav className="flex-1 space-y-2 overflow-y-auto p-4">
        {menus.map((menu) => {
          const Icon = menu.icon;

          const active =
            pathname === menu.href ||
            pathname.startsWith(menu.href + "/");

          return (
            <Link
              key={menu.href}
              href={menu.href}
              className={`flex items-center gap-3 rounded-lg px-4 py-3 transition-colors ${
                active
                  ? "bg-orange-500 text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              <Icon className="h-5 w-5" />

              <span>{menu.name}</span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}