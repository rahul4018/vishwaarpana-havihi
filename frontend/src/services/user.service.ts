import api from "@/lib/api";
import {
  User,
  CreateUserRequest,
  UpdateUserRequest,
} from "@/types/user.types";

const BASE_URL = "/users";

class UserService {
  async getAll(): Promise<User[]> {
    const response = await api.get<User[]>(BASE_URL);
    return response.data;
  }

  async getById(id: string): Promise<User> {
    const response = await api.get<User>(`${BASE_URL}/${id}`);
    return response.data;
  }

  async create(data: CreateUserRequest): Promise<User> {
    const response = await api.post<User>(BASE_URL, data);
    return response.data;
  }

  async update(
    id: string,
    data: UpdateUserRequest
  ): Promise<User> {
    const response = await api.put<User>(
      `${BASE_URL}/${id}`,
      data
    );
    return response.data;
  }

  async delete(id: string): Promise<void> {
    await api.delete(`${BASE_URL}/${id}`);
  }
}

export default new UserService();