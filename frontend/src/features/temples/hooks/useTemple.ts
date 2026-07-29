import { useQuery } from "@tanstack/react-query";

import { templeService } from "../services/temple.service";

export function useTemple(id: string) {
  return useQuery({
    queryKey: ["temples", id],
    queryFn: () => templeService.getById(id),
    enabled: !!id,
  });
}