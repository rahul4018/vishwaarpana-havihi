import { api } from "@/services/api";
import type { DashboardResponse } from "./dashboard.types";

export const dashboardService = {
  getStats: async (): Promise<DashboardResponse> => {
    const response = await api.get("/dashboard/stats");
    return response.data;
  },
};