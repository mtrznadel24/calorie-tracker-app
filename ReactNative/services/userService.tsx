import { api } from "@/api/axiosInstance";

const userService = {
  updateProfile: async (data: { height: number | null; age: number | null; gender: string | null }) => {
    const response = await api.put("/user/me", data);
    return response.data;
  }
};

export default userService;