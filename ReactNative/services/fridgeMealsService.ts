import {api} from "@/api/axiosInstance";


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

export interface AddMealData {
  name: string;
  is_favourite?: boolean;
}

export interface UpdateMealData {
  name?: string;
  is_favourite?: boolean;
}

const fridgeMealsService = {
  addMeal: async (data: AddMealData) => {
    const response = await api.post('/fridge/meals', data);
    return response.data;
  },
  getMeals: async () => {
    const response = await api.get('/fridge/meals');
    return response.data;
  },
  updateMeal: async (id: number, data: UpdateMealData) => {
    const response = await api.put(`/fridge/meals/${id}`, data);
    return response.data;
  },
  deleteMeal: async (id: number) => {
    const response = await api.delete(`/fridge/meals/${id}`);
    return response.data;
  }
}

export default fridgeMealsService;