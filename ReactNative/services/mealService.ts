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

const formatDateForApi = (date: Date): string => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

const mealService = {
  getMealLogs: async (meal_date: Date) => {

    const dateString = formatDateForApi(meal_date);
    const response = await api.get(`/meals/${dateString}/meal-logs`)
    return response.data;
  }
}

export default mealService;