import { api } from "@/services/api";

import type {
  Category,
  CategoryListResponse,
  CreateCategoryRequest,
  UpdateCategoryRequest,
} from "../types/category.types";

export const categoryService = {
  getAll: async (): Promise<CategoryListResponse> => {
    const { data } = await api.get("/categories");
    return data;
  },

  getById: async (
    id: string
  ): Promise<Category> => {
    const { data } = await api.get(
      `/categories/${id}`
    );

    return data;
  },

  create: async (
    payload: CreateCategoryRequest
  ): Promise<Category> => {
    const { data } = await api.post(
      "/categories",
      payload
    );

    return data;
  },

  update: async (
    id: string,
    payload: UpdateCategoryRequest
  ): Promise<Category> => {
    const { data } = await api.put(
      `/categories/${id}`,
      payload
    );

    return data;
  },

  delete: async (
    id: string
  ): Promise<void> => {
    await api.delete(`/categories/${id}`);
  },
};