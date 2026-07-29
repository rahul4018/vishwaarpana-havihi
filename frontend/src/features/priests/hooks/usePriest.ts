import { useQuery } from "@tanstack/react-query";

import { priestService } from "../services/priest.service";

export function usePriest(id: string) {
  return useQuery({
    queryKey: ["priests", id],
    queryFn: () => priestService.getById(id),
    enabled: !!id,
  });
}