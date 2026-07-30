import api from "@/lib/api";
import { Role } from "@/types/role.types";

class RoleService {
  async getAll(): Promise<Role[]> {
    const response = await api.get<Role[]>("/roles");
    return response.data;
  }
}

export default new RoleService();