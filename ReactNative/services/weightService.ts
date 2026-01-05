import { api } from "@/api/axiosInstance";

const weightService = {
  addWeight: async (data: { weight: number}) => {
    const response = await api.post("/weights", data);
    return response.data;
  }
};

export default weightService;