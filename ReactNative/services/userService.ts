import { api } from "@/api/axiosInstance";

export interface UserUpdateData {
  username?: string | null;
  height?: number | null;
  age?: number | null;
  gender?: string | null;
  activity_level?: number | null;
  target_weekly_gain?: number | null;
}

export interface EmailUpdateData {
  new_email: string;
  repeat_email: string;
}

export interface PasswordUpdateData {
  old_password: string;
  new_password: string;
  repeat_password: string;
}

export interface DeleteAccountData {
  password: string;
}

const userService = {
  updateProfile: async (data: UserUpdateData) => {
    const response = await api.put("/user/me", data);
    return response.data;
  },

  updateEmail: async (data: EmailUpdateData)=> {
    const response = await api.put("/user/me/email", data);
    return response.data;
  },

  updatePassword: async (data: PasswordUpdateData)=> {
    await api.put("/user/me/password", data);
  },

  deleteUser: async (payload: DeleteAccountData) => {
    await api.delete("/user/me", {data: payload});
  }
};

export default userService;