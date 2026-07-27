"use client";

import Link from "next/link";

import {
  NavigationMenu,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";

import { navigation } from "@/config/navigation";

import MegaMenu from "./MegaMenu";
import NavItem from "./NavItem";

export default function MainNavigation() {
  return (
    <NavigationMenu
      viewport={false}
      className="hidden lg:flex"
    >
      <NavigationMenuList>
        {navigation.map((item) => {
          if (item.id === "temple") {
            return <MegaMenu key={item.id} />;
          }

          if (item.href) {
            return (
              <Link
                key={item.id}
                href={item.href}
                className="rounded-md px-3 py-2 text-sm font-medium text-slate-700 transition-all hover:bg-slate-100 hover:text-orange-600"
              >
                {item.title}
              </Link>
            );
          }

          return (
            <NavItem
              key={item.id}
              item={item}
            />
          );
        })}
      </NavigationMenuList>
    </NavigationMenu>
  );
}