import { api } from "@/api/axiosInstance";

export interface UserUpdateData {
  username?: string | null;
  height?: number | null;
  age?: number | null;
  gender?: string | null;
  activity_level?: number | null;
  target_weekly_gain?: number | null;
}

const userService = {
  updateProfile: async (data: UserUpdateData) => {
    const response = await api.put("/user/me", data);
    return response.data;
  }
};

export default userService;