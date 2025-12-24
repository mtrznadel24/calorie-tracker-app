import {
  View,
  Text,
  TouchableWithoutFeedback,
  Keyboard,
  TextInput,
  Pressable,
  ActivityIndicator,
  useColorScheme
} from 'react-native';
import React, { useState } from 'react';
import { z } from "zod";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "expo-router";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Toast from "react-native-toast-message";
import clsx from "clsx";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";
import { Ionicons } from "@expo/vector-icons";

const registerSchema = z.object({
  username: z.string().min(3, "Username need to be at least 3 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password need to be at least 8 characters"),
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

type RegisterForm = z.infer<typeof registerSchema>;

const Register = () => {
  const { register, isLoading } = useAuth();
  const router = useRouter();
  const colorScheme = useColorScheme();

  const { control, handleSubmit, formState: { errors } } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema) as any,
    shouldUnregister: false,
    defaultValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  });

  const onSubmit = async (data: RegisterForm) => {
    try {
      await register(data);
      router.replace("/(onboarding)/setup-profile")
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Register Failed',
        text2: 'Something went wrong ❌'
      });
    }
  };

  return (
    <KeyboardAwareScrollView
      contentContainerStyle={{ flexGrow: 1 }}
      className="bg-light-50 dark:bg-dark-900"
      enableOnAndroid={true}
      extraScrollHeight={20}
      enableAutomaticScroll={true}
      keyboardShouldPersistTaps="handled"
      bounces={false}
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View className="p-6 pt-32">
          <View className="flex">
              <Text className="text-3xl font-bold mb-8 text-center text-dark-900 dark:text-text-light">
                Sign up! 👋
              </Text>

              {/* USERNAME */}
              <View className="mb-4">
                <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Username</Text>
                <Controller
                  control={control}
                  name="username"
                  render={({ field: { onChange, onBlur, value } }) => (
                    <TextInput
                      className={clsx("p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light",
                        errors.username ? "border-state-error" : "border-light-300 dark:border-dark-600")}
                      placeholder="username"
                      placeholderTextColor="#9CA3AF"
                      onBlur={onBlur}
                      onChangeText={onChange}
                      value={value}
                      autoCapitalize="none"
                    />
                  )}
                />
                {errors.username && <Text className="text-state-error text-xs mt-1 ml-1">{errors.username.message}</Text>}
              </View>

              {/* EMAIL */}
              <View className="mb-4">
                <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Email</Text>
                <Controller
                  control={control}
                  name="email"
                  render={({ field: { onChange, onBlur, value } }) => (
                    <TextInput
                      className={clsx("p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light",
                        errors.email ? "border-state-error" : "border-light-300 dark:border-dark-600")}
                      placeholder="email"
                      placeholderTextColor="#9CA3AF"
                      onBlur={onBlur}
                      onChangeText={onChange}
                      value={value}
                      autoCapitalize="none"
                      keyboardType="email-address"
                    />
                  )}
                />
                {errors.email && <Text className="text-state-error text-xs mt-1 ml-1">{errors.email.message}</Text>}
              </View>

              {/* PASSWORD */}
              <View className="mb-6">
                <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Password</Text>
                <Controller
                  control={control}
                  name="password"
                  render={({ field: { onChange, onBlur, value } }) => (
                    <TextInput
                      className={clsx("p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light",
                        errors.password ? "border-state-error" : "border-light-300 dark:border-dark-600")}
                      placeholder="password"
                      placeholderTextColor="#9CA3AF"
                      onBlur={onBlur}
                      onChangeText={onChange}
                      value={value}
                      secureTextEntry={true}
                    />
                  )}
                />
                {errors.password && <Text className="text-state-error text-xs mt-1 ml-1">{errors.password.message}</Text>}
              </View>

              {/* CONFIRM PASSWORD */}
              <View className="mb-6">
                <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Confirm Password</Text>
                <Controller
                  control={control}
                  name="confirmPassword"
                  render={({ field: { onChange, onBlur, value } }) => (
                    <TextInput
                      className={clsx("p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light",
                        errors.confirmPassword ? "border-state-error" : "border-light-300 dark:border-dark-600")}
                      placeholder="password"
                      placeholderTextColor="#9CA3AF"
                      onBlur={onBlur}
                      onChangeText={onChange}
                      value={value}
                      secureTextEntry={true}
                    />
                  )}
                />
                {errors.confirmPassword && <Text className="text-state-error text-xs mt-1 ml-1">{errors.confirmPassword.message}</Text>}
              </View>

              {/* NEXT BUTTON */}
              <Pressable onPress={handleSubmit(onSubmit)} className="p-4 rounded-xl items-center shadow-sm bg-primary">
                <Text className="text-white font-bold text-lg">Sign up</Text>
              </Pressable>

              <View className="mt-8 flex-row justify-center">
                <Text className="text-dark-700 dark:text-text-muted">Have an account? </Text>
                <Pressable onPress={() => router.push("/(auth)/login")}>
                  <Text className="font-bold text-primary">Sign in</Text>
                </Pressable>
              </View>
          </View>

        </View>
      </TouchableWithoutFeedback>
    </KeyboardAwareScrollView>
  );
};

export default Register;