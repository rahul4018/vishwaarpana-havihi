"use client";

import { Bell } from "lucide-react";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export default function NotificationPanel() {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <button
          type="button"
          className="relative flex h-10 w-10 items-center justify-center rounded-lg border bg-white transition hover:bg-slate-100"
        >
          <Bell className="h-5 w-5" />

          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500" />
        </button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-80">
        <DropdownMenuLabel>Notifications</DropdownMenuLabel>

        <DropdownMenuSeparator />

        <DropdownMenuItem>
          New booking received
        </DropdownMenuItem>

        <DropdownMenuItem>
          Donation received
        </DropdownMenuItem>

        <DropdownMenuItem>
          Inventory running low
        </DropdownMenuItem>

        <DropdownMenuItem>
          Festival tomorrow
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}