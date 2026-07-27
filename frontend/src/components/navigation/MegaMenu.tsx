"use client";

import {
  Building2,
  CalendarDays,
  ClipboardList,
  Clock3,
  HeartHandshake,
  Image,
  PartyPopper,
  Sparkles,
  Users,
} from "lucide-react";

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
        <div className="grid w-[850px] grid-cols-3 gap-8 p-8">
          <MegaMenuSection
            title="Temple Management"
            items={[
              {
                title: "Temple Information",
                description: "Manage temple profile and basic information",
                href: "/temple",
                icon: <Building2 className="h-5 w-5" />,
              },
              {
                title: "Temple Timings",
                description: "Configure opening hours and schedules",
                href: "/temple/timings",
                icon: <Clock3 className="h-5 w-5" />,
              },
              {
                title: "Gallery",
                description: "Manage temple photos and media",
                href: "/gallery",
                icon: <Image className="h-5 w-5" />,
              },
            ]}
          />

          <MegaMenuSection
            title="Priest Management"
            items={[
              {
                title: "Priests",
                description: "Manage priest profiles and assignments",
                href: "/priests",
                icon: <Users className="h-5 w-5" />,
              },
              {
                title: "Attendance",
                description: "Track priest attendance records",
                href: "/attendance",
                icon: <ClipboardList className="h-5 w-5" />,
              },
              {
                title: "Schedule",
                description: "Manage priest schedules and availability",
                href: "/schedule",
                icon: <CalendarDays className="h-5 w-5" />,
              },
            ]}
          />

          <MegaMenuSection
            title="Services"
            items={[
              {
                title: "Poojas",
                description: "Manage pooja offerings and pricing",
                href: "/poojas",
                icon: <Sparkles className="h-5 w-5" />,
              },
              {
                title: "Festivals",
                description: "Organize temple festivals and events",
                href: "/festivals",
                icon: <PartyPopper className="h-5 w-5" />,
              },
              {
                title: "Donations",
                description: "Track donations and contributions",
                href: "/donations",
                icon: <HeartHandshake className="h-5 w-5" />,
              },
            ]}
          />
        </div>
      </NavigationMenuContent>
    </NavigationMenuItem>
  );
}