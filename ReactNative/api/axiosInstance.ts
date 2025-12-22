import axios from "axios";
import {tokenStorage} from "@/core/tokenStorage";


const BASE_URL = process.env.EXPO_PUBLIC_API_URL;

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

axios.interceptors.request.use(
  async (config) => {
    const token = await tokenStorage.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
          const refreshToken = await tokenStorage.getRefreshToken();
          if (!refreshToken) throw new Error('Brak refresh tokena');

          const response = await axios.post(`${BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token, refresh_token: newRefreshToken } = response.data;

          await tokenStorage.setTokens(access_token, newRefreshToken);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);

        } catch (refreshError) {
          await tokenStorage.deleteTokens();
          return Promise.reject(refreshError);
        }
    }

    return Promise.reject(error);
  }
)

