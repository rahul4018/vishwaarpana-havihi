"use client";

import {
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";

import MegaMenuSection from "./MegaMenuSection";

export default function MegaMenu() {
  return (
    <NavigationMenuItem>
      <NavigationMenuTrigger>
        Temple
      </NavigationMenuTrigger>

      <NavigationMenuContent>
        <div className="grid grid-cols-3 gap-8 p-6 w-[720px]">
          <MegaMenuSection
            title="Temple Management"
            items={[
              {
                title: "Temple Information",
                href: "/temple",
              },
              {
                title: "Temple Timings",
                href: "/temple/timings",
              },
              {
                title: "Gallery",
                href: "/gallery",
              },
            ]}
          />

          <MegaMenuSection
            title="Priest Management"
            items={[
              {
                title: "Priests",
                href: "/priests",
              },
              {
                title: "Attendance",
                href: "/attendance",
              },
              {
                title: "Schedule",
                href: "/schedule",
              },
            ]}
          />

          <MegaMenuSection
            title="Services"
            items={[
              {
                title: "Poojas",
                href: "/poojas",
              },
              {
                title: "Festivals",
                href: "/festivals",
              },
              {
                title: "Donations",
                href: "/donations",
              },
            ]}
          />
        </div>
      </NavigationMenuContent>
    </NavigationMenuItem>
  );
}