"use client";

import { navigation } from "@/config/navigation";

import NavItem from "./NavItem";

export default function MainNavigation() {
  return (
    <nav className="hidden items-center gap-1 lg:flex">
      {navigation.map((item) => (
        <NavItem
          key={item.id}
          item={item}
        />
      ))}
    </nav>
  );
}