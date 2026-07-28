"use client";

import {
  Building2,
  CalendarDays,
  ClipboardList,
  Clock3,
  HeartHandshake,
  Image,
  LucideIcon,
  Package,
  PartyPopper,
  Receipt,
  Settings,
  Sparkles,
  Users,
} from "lucide-react";

import {
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";

import type {
  NavigationSection,
  UserRole,
} from "@/types/navigation";

import MegaMenuSection from "./MegaMenuSection";

interface MegaMenuProps {
  title: string;
  sections: NavigationSection[];
}

const iconMap: Record<string, LucideIcon> = {
  Building2,
  CalendarDays,
  ClipboardList,
  Clock3,
  HeartHandshake,
  Image,
  Package,
  PartyPopper,
  Receipt,
  Settings,
  Sparkles,
  Users,
};

export default function MegaMenu({
  title,
  sections,
}: MegaMenuProps) {
  /**
   * TODO:
   * Replace with logged-in user's role.
   * Example:
   * const currentRole = user.role;
   */
  const currentRole: UserRole = "admin";

  const filteredSections = sections
    .map((section) => ({
      ...section,
      children: section.children.filter((child) =>
        child.roles.includes(currentRole)
      ),
    }))
    .filter((section) => section.children.length > 0);

  if (filteredSections.length === 0) {
    return null;
  }

  return (
    <NavigationMenuItem>
      <NavigationMenuTrigger>
        {title}
      </NavigationMenuTrigger>

      <NavigationMenuContent>
        <div
          className="grid gap-8 p-8"
          style={{
            gridTemplateColumns: `repeat(${filteredSections.length}, minmax(240px, 1fr))`,
            minWidth: `${Math.max(filteredSections.length * 280, 850)}px`,
          }}
        >
          {filteredSections.map((section) => (
            <MegaMenuSection
              key={section.title}
              title={section.title}
              items={section.children.map((child) => {
                const Icon =
                  iconMap[child.icon] ?? Building2;

                return {
                  title: child.title,
                  description: child.description,
                  href: child.href,
                  icon: (
                    <Icon className="h-5 w-5 text-orange-500" />
                  ),
                };
              })}
            />
          ))}
        </div>
      </NavigationMenuContent>
    </NavigationMenuItem>
  );
}