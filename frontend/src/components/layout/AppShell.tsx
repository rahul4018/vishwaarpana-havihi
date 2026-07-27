import type { ReactNode } from "react";

import MainNavigation from "@/components/navigation/MainNavigation";

interface AppShellProps {
  children: ReactNode;
}

export default function AppShell({
  children,
}: AppShellProps) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white shadow-sm">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-slate-900">
              Vishwaarpana Havihi
            </h1>
          </div>

          {/* Navigation */}
          <MainNavigation />

          {/* Right Actions */}
          <div className="flex items-center gap-3">
            <button
              type="button"
              className="rounded-md border px-3 py-1.5 text-sm transition-colors hover:bg-slate-100"
            >
              Search
            </button>

            <button
              type="button"
              className="rounded-md border px-3 py-1.5 text-sm transition-colors hover:bg-slate-100"
            >
              Notifications
            </button>

            <button
              type="button"
              className="rounded-md border px-3 py-1.5 text-sm font-medium transition-colors hover:bg-slate-100"
            >
              Rahul
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl p-6">
        {children}
      </main>
    </div>
  );
}