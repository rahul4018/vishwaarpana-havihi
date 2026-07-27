"use client";

import Link from "next/link";
import { ChevronRight } from "lucide-react";

export interface MegaMenuItem {
  title: string;
  description: string;
  href: string;
  icon?: React.ReactNode;
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
    <div className="min-w-[240px]">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-slate-900">
        {title}
      </h3>

      <div className="space-y-2">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="group flex items-start gap-3 rounded-xl p-3 transition-all duration-200 hover:bg-orange-50"
          >
            <div className="mt-1 flex h-9 w-9 items-center justify-center rounded-lg bg-orange-100 text-orange-600">
              {item.icon}
            </div>

            <div className="flex-1">
              <div className="flex items-center justify-between">
                <p className="font-medium text-slate-900 group-hover:text-orange-600">
                  {item.title}
                </p>

                <ChevronRight className="h-4 w-4 opacity-0 transition group-hover:translate-x-1 group-hover:opacity-100" />
              </div>

              <p className="mt-1 text-sm text-slate-500">
                {item.description}
              </p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}