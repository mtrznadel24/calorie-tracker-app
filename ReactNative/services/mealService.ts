import {api} from "@/api/axiosInstance";


export interface MealLog{
  id: number;
  name: string;
  type: string;
  calories: number;
  proteins: number;
  fats: number;
  carbs: number;
  weight: number;
}

export interface AddMealLogData {
  name: string;
  type: string;
  calories: number;
  proteins: number;
  fats: number;
  carbs: number;
  weight: number;
}

export interface SimpleProductData {
  name: string;
  weight: number;
  calories_100g: number;
  proteins_100g: number;
  fats_100g: number;
  carbs_100g: number;
}

export interface QuickAddLogData {
  name: string;
  date: string;
  type: string;
  calories: number;
  proteins: number;
  fats: number;
  carbs: number;
  weight: number;
}

export interface FromProductAddLogData {
  fridge_product_id: number;
  date: string;
  type: string;
  weight: number;
}

export const formatDateForApi = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const mealService = {
  quickCreateMealLog: async (data: QuickAddLogData) => {
    const response = await api.post("/meals/quick", data);
    return response.data;
  },

  fromProductCreateMealLog: async (data: FromProductAddLogData) => {
    const response = await api.post(`/meals/from-product`, data);
    return response.data;
  },

  getMealLogs: async (log_date: Date) => {

    const dateString = formatDateForApi(log_date);
    const response = await api.get(`/meals/${dateString}/meal-logs`)
    return response.data;
  }
}

export default mealService;