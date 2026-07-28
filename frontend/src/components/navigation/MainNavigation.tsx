"use client";

import Link from "next/link";

import {
  NavigationMenu,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";

import { navigation } from "@/config/navigation";
import type { UserRole } from "@/types/navigation";

import MegaMenu from "./MegaMenu";

export default function MainNavigation() {
  /**
   * TODO:
   * Replace with authenticated user's role
   * Example:
   * const currentRole = user.role;
   */
  const currentRole: UserRole = "admin";

  const filteredNavigation = navigation.filter((item) =>
    item.roles.includes(currentRole)
  );

  return (
    <NavigationMenu
      viewport={false}
      className="hidden lg:flex"
    >
      <NavigationMenuList>
        {filteredNavigation.map((item) => {
          // Mega Menu
          if (item.sections && item.sections.length > 0) {
            return (
              <MegaMenu
                key={item.id}
                title={item.title}
                sections={item.sections}
              />
            );
          }

          // Normal Link
          return (
            <Link
              key={item.id}
              href={item.href ?? "#"}
              className="rounded-md px-3 py-2 text-sm font-medium text-slate-700 transition-all hover:bg-slate-100 hover:text-orange-600"
            >
              {item.title}
            </Link>
          );
        })}
      </NavigationMenuList>
    </NavigationMenu>
  );
}