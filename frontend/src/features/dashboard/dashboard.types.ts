export interface DashboardStats {
  total_temples: number;
  total_priests: number;
  total_poojas: number;
  total_bookings: number;
  total_revenue: number;
}

export interface DashboardResponse {
  success: boolean;
  data: DashboardStats;
}