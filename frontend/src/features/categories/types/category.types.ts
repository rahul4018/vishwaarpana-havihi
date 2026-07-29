export interface Category {
  id: string;
  temple_id: string;

  name: string;
  slug: string;
  description: string | null;

  display_order: number;

  is_active: boolean;
}

export type CategoryListResponse = Category[];

export interface CreateCategoryRequest {
  temple_id: string;

  name: string;
  slug: string;
  description?: string;

  display_order: number;
}

export interface UpdateCategoryRequest {
  name?: string;
  slug?: string;
  description?: string;

  display_order?: number;

  is_active?: boolean;
}