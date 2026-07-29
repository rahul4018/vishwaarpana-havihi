"use client";

import { ReactNode } from "react";

import AppSidebar from "./AppSidebar";
import TopNavbar from "./TopNavbar";

interface DashboardLayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <AppSidebar />

      <div className="flex flex-1 flex-col">
        <TopNavbar />

        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
}