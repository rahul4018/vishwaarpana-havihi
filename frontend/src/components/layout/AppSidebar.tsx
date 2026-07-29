"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const menus = [
  { name: "Dashboard", href: "/dashboard" },
  { name: "Temples", href: "/temples" },
  { name: "Priests", href: "/priests" },
  { name: "Poojas", href: "/poojas" },
  { name: "Bookings", href: "/bookings" },
  { name: "Payments", href: "/payments" },
  { name: "Users", href: "/users" },
  { name: "Gallery", href: "/gallery" },
  { name: "Settings", href: "/settings" },
];

export default function AppSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-white h-screen sticky top-0">
      <div className="border-b p-6">
        <h1 className="text-xl font-bold">
          Vishwaarpana
        </h1>

        <p className="text-sm text-gray-500">
          Admin Panel
        </p>
      </div>

      <nav className="flex flex-col p-4 gap-2">
        {menus.map((menu) => (
          <Link
            key={menu.href}
            href={menu.href}
            className={`rounded-lg px-4 py-3 transition ${
              pathname === menu.href
                ? "bg-orange-500 text-white"
                : "hover:bg-gray-100"
            }`}
          >
            {menu.name}
          </Link>
        ))}
      </nav>
    </aside>
  );
}