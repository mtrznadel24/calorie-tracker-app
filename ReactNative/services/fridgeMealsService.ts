import {api} from "@/api/axiosInstance";
import {data} from "browserslist";


export interface Meal {
  id: number;
  name: string;
  calories: number;
  proteins: number;
  fats: number;
  carbs: number;
  products_count: number;
  is_favourite: boolean;
}

export interface Ingredient {
  weight: number;
  fridge_product_id: number;
}

export interface IngredientDisplayItem {
  tempId?: string;
  id?: number;
  fridge_product_id: number;
  weight: number;
  product_name: string;
  calories: number;
}

export interface AddMealData {
  name: string;
  is_favourite?: boolean;
  ingredients: Ingredient[];
}

export interface UpdateMealData {
  name?: string;
  is_favourite?: boolean;
}

export interface AddIngredientData {
  weight: number;
  fridge_product_id: number;
}

const fridgeMealsService = {
  addMealWithIngredients: async (data: AddMealData) => {
    const response = await api.post("/fridge/meals", data);
    return response.data;
  },

  getMeals: async () => {
    const response = await api.get('/fridge/meals');
    return response.data;
  },

  getMealById: async (id: number) => {
    const response = await api.get(`/fridge/meals/${id}`);
    return response.data;
  },

  updateMeal: async (id: number, data: UpdateMealData) => {
    const response = await api.put(`/fridge/meals/${id}`, data);
    return response.data;
  },

  deleteMeal: async (id: number) => {
    const response = await api.delete(`/fridge/meals/${id}`);
    return response.data;
  },

  addFridgeMealIngredient: async (id: number, data: AddIngredientData)=> {
    const response = await api.post(`/fridge/meals/${id}/ingredients`, data)
    return response.data;
  },

  getMealIngredients: async (id: number) => {
    const response = await api.get(`/fridge/meals/${id}/ingredients`);
    return response.data;
  },

  deleteMealIngredient: async (meal_id: number, id: number)=> {
    const response = await api.delete(`/fridge/meals/${meal_id}/ingredients/${id}`);
    return response.data;
  }
}

export default fridgeMealsService;