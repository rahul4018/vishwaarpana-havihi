import { useQuery } from "@tanstack/react-query";

import { dashboardService } from "./dashboard.service";

export function useDashboardStats() {
  return useQuery({
    queryKey: ["dashboard", "stats"],
    queryFn: dashboardService.getStats,
  });
}