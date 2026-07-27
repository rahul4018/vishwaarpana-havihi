"use client";

import { ReactNode } from "react";

import QueryProvider from "./QueryProvider";
import ThemeProvider from "./ThemeProvider";

interface Props {
  children: ReactNode;
}

export default function AppProvider({
  children,
}: Props) {
  return (
    <ThemeProvider>
      <QueryProvider>
        {children}
      </QueryProvider>
    </ThemeProvider>
  );
}