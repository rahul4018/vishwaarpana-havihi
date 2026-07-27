"use client";

import { Search } from "lucide-react";

export default function SearchBar() {
  return (
    <button
      type="button"
      aria-label="Search"
      className="
        flex
        h-10
        w-64
        items-center
        justify-between
        rounded-xl
        border
        border-slate-200
        bg-white
        px-3
        text-sm
        text-slate-500
        shadow-sm
        transition-all
        duration-200
        hover:border-orange-400
        hover:shadow-md
        focus:outline-none
        focus:ring-2
        focus:ring-orange-500/30
      "
    >
      <div className="flex items-center gap-2">
        <Search className="h-4 w-4 text-slate-400" />

        <span>Search modules...</span>
      </div>

      <kbd className="rounded-md border border-slate-200 bg-slate-50 px-2 py-1 text-[11px] font-medium text-slate-500">
        Ctrl K
      </kbd>
    </button>
  );
}