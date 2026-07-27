"use client";

import Link from "next/link";
import { ChevronDown } from "lucide-react";

interface NavigationLinkProps {
  title: string;
  href?: string;
  hasDropdown?: boolean;
  active?: boolean;
}

export default function NavigationLink({
  title,
  href,
  hasDropdown = false,
  active = false,
}: NavigationLinkProps) {
  const className = `
    flex items-center gap-1 rounded-md px-3 py-2
    text-sm font-medium transition-all duration-200
    ${
      active
        ? "bg-orange-50 text-orange-600"
        : "text-slate-700 hover:bg-slate-100 hover:text-orange-600"
    }
  `;

  if (href) {
    return (
      <Link href={href} className={className}>
        <span>{title}</span>

        {hasDropdown && (
          <ChevronDown className="h-4 w-4" />
        )}
      </Link>
    );
  }

  return (
    <button type="button" className={className}>
      <span>{title}</span>

      {hasDropdown && (
        <ChevronDown className="h-4 w-4" />
      )}
    </button>
  );
}