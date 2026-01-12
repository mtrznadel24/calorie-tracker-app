import { api } from "@/api/axiosInstance";

export interface Weight {
  id: number,
  date: string,
  weight: number
}

export interface WeightCreate {
  weight: number
}

const weightService = {
  addWeight: async (data: WeightCreate) => {
    const response = await api.post("/weights", data);
    return response.data;
  },

  async getUserWeights() {
    const response = await api.get("/weights");
    return response.data;
  },

  async deleteWeight(id: number) {
    const response = await api.delete(`/weights/${id}`)
  }

};

export default weightService;