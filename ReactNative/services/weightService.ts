import { api } from "@/api/axiosInstance";

const weightService = {
  createWeight: async (data: { weight: number | null }) => {
    const response = await api.post("/weights", data);
    return response.data;
  }
};

export default weightService;