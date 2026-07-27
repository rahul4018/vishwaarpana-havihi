"use client";

import Link from "next/link";

import { navigation } from "@/config/navigation";

export default function MainNavigation() {
  return (
    <nav className="flex items-center gap-8">
      {navigation.map((item) => (
        <div key={item.id}>
          {item.href ? (
            <Link
              href={item.href}
              className="text-sm font-medium text-slate-700 transition-colors hover:text-orange-600"
            >
              {item.title}
            </Link>
          ) : (
            <button
              type="button"
              className="text-sm font-medium text-slate-700 transition-colors hover:text-orange-600"
            >
              {item.title}
            </button>
          )}
        </div>
      ))}
    </nav>
  );
}