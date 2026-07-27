"use client";

import Link from "next/link";
import { ChevronDown } from "lucide-react";

import type { NavigationItem } from "@/types/navigation";

interface NavItemProps {
  item: NavigationItem;
}

export default function NavItem({
  item,
}: NavItemProps) {
  // Normal navigation item
  if (item.href) {
    return (
      <Link
        href={item.href}
        className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition-all duration-200 hover:bg-slate-100 hover:text-orange-600"
      >
        {item.title}
      </Link>
    );
  }

  // Future Mega Menu
  return (
    <button
      type="button"
      className="flex items-center gap-1 rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition-all duration-200 hover:bg-slate-100 hover:text-orange-600"
    >
      <span>{item.title}</span>

      <ChevronDown className="h-4 w-4 transition-transform duration-200" />
    </button>
  );
}