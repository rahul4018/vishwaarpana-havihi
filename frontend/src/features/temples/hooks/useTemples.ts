import { useQuery } from "@tanstack/react-query";

import { templeService } from "../services/temple.service";

export function useTemples() {
  return useQuery({
    queryKey: ["temples"],
    queryFn: templeService.getAll,
  });
}