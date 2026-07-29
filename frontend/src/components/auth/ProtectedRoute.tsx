"use client";

import { ReactNode, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";

import { useAuthStore } from "@/store/auth.store";
import {
  hasPermission,
  UserRole,
} from "@/lib/permissions";

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({
  children,
}: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();

  const user = useAuthStore((state) => state.user);

  useEffect(() => {
    if (!user) {
      router.replace("/login");
      return;
    }

    const role = user.role as UserRole;

    if (!hasPermission(role, pathname)) {
      router.replace("/dashboard");
    }
  }, [pathname, router, user]);

  if (!user) {
    return null;
  }

  const role = user.role as UserRole;

  if (!hasPermission(role, pathname)) {
    return null;
  }

  return <>{children}</>;
}