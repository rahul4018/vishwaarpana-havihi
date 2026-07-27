"use client";

import { ReactNode } from "react";
import {
  QueryClientProvider,
} from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

import { queryClient } from "@/config/query-client";
import { env } from "@/config/env";

interface Props {
  children: ReactNode;
}

export default function QueryProvider({
  children,
}: Props) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}

      {env.ENABLE_QUERY_DEVTOOLS && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}