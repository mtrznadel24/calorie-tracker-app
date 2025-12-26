import { api } from "@/api/axiosInstance";

export type FoodCategory =
  | "fruits"
  | "vegetables"
  | "grains"
  | "dairy"
  | "meat and fish"
  | "plant protein"
  | "fats"
  | "drinks"
  | "snacks";

export interface Product {
  id: number;
  product_name: string;
  category: string;
  is_favourite: boolean;
  calories_100g: number;
  proteins_100g: number;
  fats_100g: number;
  carbs_100g: number;
}

export interface AddProductData {
  product_name: string;
  calories_100g?: number;
  proteins_100g?: number;
  fats_100g?: number;
  carbs_100g?: number;
  category?: FoodCategory;
  is_favourite?: boolean;
}

export interface UpdateProductData {
  product_name?: string;
  calories_100g?: number;
  proteins_100g?: number;
  fats_100g?: number;
  carbs_100g?: number;
  category?: FoodCategory;
  is_favourite?: boolean;
}

const fridgeProductsService = {
  addProduct: async (data: AddProductData) => {
    const response = await api.post("/fridge/products", data);
    return response.data;
  },

  getProducts: async () => {
    const response = await api.get("/fridge/products");
    return response.data;
  },

  updateProduct: async (id: number, data: UpdateProductData) => {
    const response = await api.put(`/fridge/products/${id}`, data)
    return response.data;
  },

  deleteProduct: async (id: number) => {
    const response = await api.delete(`/fridge/products/${id}`);
    return response.data;
  }
};

export default fridgeProductsService;