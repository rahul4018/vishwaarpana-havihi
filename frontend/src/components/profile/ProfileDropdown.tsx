"use client";

import { useRouter } from "next/navigation";
import {
  User,
  Settings,
  LogOut,
  Moon,
  CircleHelp,
} from "lucide-react";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/auth.store";

export default function ProfileDropdown() {
  const router = useRouter();

  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();

    router.replace("/login");
    router.refresh();
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">
          Rahul
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        className="w-64"
      >
        <DropdownMenuLabel>
          <div className="space-y-1">
            <p className="font-semibold">
              Admin
            </p>

            <p className="text-xs text-muted-foreground">
              vishwaarpana-havihi
            </p>
          </div>
        </DropdownMenuLabel>

        <DropdownMenuSeparator />

        <DropdownMenuItem>
          <User className="mr-2 h-4 w-4" />
          My Profile
        </DropdownMenuItem>

        <DropdownMenuItem>
          <Settings className="mr-2 h-4 w-4" />
          Account Settings
        </DropdownMenuItem>

        <DropdownMenuItem>
          <Moon className="mr-2 h-4 w-4" />
          Theme
        </DropdownMenuItem>

        <DropdownMenuItem>
          <CircleHelp className="mr-2 h-4 w-4" />
          Help
        </DropdownMenuItem>

        <DropdownMenuSeparator />

        <DropdownMenuItem
          onClick={handleLogout}
          className="cursor-pointer text-red-600 focus:text-red-600"
        >
          <LogOut className="mr-2 h-4 w-4" />
          Logout
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}