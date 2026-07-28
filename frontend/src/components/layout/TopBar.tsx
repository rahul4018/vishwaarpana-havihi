"use client";

import MainNavigation from "@/components/navigation/MainNavigation";
import NotificationPanel from "@/components/notification/NotificationPanel";
import ProfileDropdown from "@/components/profile/ProfileDropdown";
import SearchBar from "@/components/search/SearchBar";

export default function TopBar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-white/95 shadow-sm backdrop-blur supports-[backdrop-filter]:bg-white/80">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-500 text-lg font-bold text-white shadow-sm">
            ॐ
          </div>

          <div className="leading-tight">
            <h1 className="text-lg font-bold text-slate-900">
              Vishwaarpana Havihi
            </h1>

            <p className="text-xs text-slate-500">
              Temple ERP Platform
            </p>
          </div>
        </div>

        {/* Navigation */}
        <MainNavigation />

        {/* Right Actions */}
        <div className="flex items-center gap-3">
          <SearchBar />

          <NotificationPanel />

          <ProfileDropdown />
        </div>
      </div>
    </header>
  );
}