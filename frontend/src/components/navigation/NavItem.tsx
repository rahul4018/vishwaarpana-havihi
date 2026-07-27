"use client";

import type { NavigationItem } from "@/types/navigation";

import NavigationLink from "./NavigationLink";

interface NavItemProps {
  item: NavigationItem;
}

export default function NavItem({
  item,
}: NavItemProps) {
  return (
    <NavigationLink
      title={item.title}
      href={item.href}
      hasDropdown={!!item.sections}
    />
  );
}