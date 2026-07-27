"use client";

import Link from "next/link";

export interface MegaMenuItem {
  title: string;
  href: string;
}

interface MegaMenuSectionProps {
  title: string;
  items: MegaMenuItem[];
}

export default function MegaMenuSection({
  title,
  items,
}: MegaMenuSectionProps) {
  return (
    <div className="min-w-[220px]">
      <h3 className="mb-3 text-sm font-semibold text-slate-900">
        {title}
      </h3>

      <div className="space-y-1">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="block rounded-md px-3 py-2 text-sm text-slate-600 transition-colors hover:bg-orange-50 hover:text-orange-600"
          >
            {item.title}
          </Link>
        ))}
      </div>
    </div>
  );
}