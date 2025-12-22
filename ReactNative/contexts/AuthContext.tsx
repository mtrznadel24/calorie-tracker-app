import React, { useState, createContext, useContext, useEffect } from "react";
import { tokenStorage } from "@/core/tokenStorage";
import { api } from "@/api/axiosInstance";

export interface RegisterFormData {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
  height: number | null;
  age: number | null;
  gender: string | null;
}

interface AuthContextType {
  user: any;
  isLoading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  register: (data: RegisterFormData) => Promise<void>;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const accessToken = await tokenStorage.getAccessToken();
        if (accessToken) {
          const response = await api.get("/user/me");
          setUser(response.data);
        }
      } catch (e) {
        console.log("Error occurred while fetching user", e);
        await tokenStorage.deleteTokens();
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    checkLoginStatus();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post("/auth/login", formData.toString(), {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const { access_token, refresh_token } = response.data;

      await tokenStorage.setTokens(access_token, refresh_token);

      const userResponse = await api.get("/user/me");
      setUser(userResponse.data);
    } catch (e) {
      console.log("Login error", e);
      throw e;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterFormData) => {
    setIsLoading(true);

    try {
      const payload = {
        ...data,
        confirm_password: data.confirmPassword,
        activity_level: null,
      };

      const response = await api.post("/auth/register", payload);
      const { access_token, refresh_token } = response.data;
      await tokenStorage.setTokens(access_token, refresh_token);
      const userResponse = await api.get("/user/me");
      setUser(userResponse.data);
    } catch (e) {
      console.log("Register error", e);
      throw e;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);

    try {
      const refreshToken = await tokenStorage.getRefreshToken();
      if (refreshToken) {
        await api.post("/auth/logout", { refresh_token: refreshToken });
      }
      await tokenStorage.deleteTokens();
      setUser(null);
    } catch (e) {
      console.log("Logout error", e);
      await tokenStorage.deleteTokens();
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
};
