import {
  View, Text, Alert, TextInput, Pressable, ActivityIndicator, KeyboardAvoidingView, Platform,
  TouchableWithoutFeedback, Keyboard, Animated
} from 'react-native'
import React from 'react'
import {z} from "zod";
import {useAuth} from "@/contexts/AuthContext";
import {useRouter} from "expo-router";
import {Controller, useForm} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import clsx from "clsx";
import ScrollView = Animated.ScrollView;
import Toast from "react-native-toast-message";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters long")
})

type LoginForm = z.infer<typeof loginSchema>;

const Login = () => {
  const { login, isLoading } = useAuth();
  const router = useRouter();

  const { control, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: '',
      password: ''
    }
  });

  const onSubmit = async (data: LoginForm) => {
    try {
      await login(data.email, data.password);
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Login Failed',
        text2: 'Incorrect email or password ❌'
      });
    }
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      className="flex-1 bg-light-50 dark:bg-dark-900"
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <ScrollView
          contentContainerStyle={{ flexGrow: 1, justifyContent: 'center' }}
          className="p-6"
          keyboardShouldPersistTaps="handled"
        >

          <Text className="text-3xl font-bold mb-8 text-center text-dark-900 dark:text-text-light">
            Welcome! 👋
          </Text>


          {/* EMAIL INPUT */}
          <View className="mb-4">
            <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">
              Email
            </Text>
            <Controller
              control={control}
              name="email"
              render={({ field: { onChange, onBlur, value } }) => (
                <TextInput
                  className={clsx(
                    "p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light",
                    errors.email
                      ? "border-state-error"
                      : "border-light-300 dark:border-dark-600"
                  )}
                  placeholder="example@email.com"
                  placeholderTextColor="#9CA3AF"
                  onBlur={onBlur}
                  onChangeText={onChange}
                  value={value}
                  autoCapitalize="none"
                  keyboardType="email-address"
                  autoComplete="email"
                />
              )}
            />
            {errors.email && (
              <Text className="text-state-error text-xs mt-1 ml-1">
                {errors.email.message}
              </Text>
            )}
          </View>

          {/* PASSWORD INPUT */}
          <View className="mb-6">
            <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">
              Password
            </Text>
            <Controller
              control={control}
              name="password"
              render={({ field: { onChange, onBlur, value } }) => (
                <TextInput
                  className={clsx(
                    "p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light",
                    errors.password
                      ? "border-state-error"
                      : "border-light-300 dark:border-dark-600"
                  )}
                  placeholder="••••••••"
                  placeholderTextColor="#9CA3AF"
                  onBlur={onBlur}
                  onChangeText={onChange}
                  value={value}
                  secureTextEntry
                />
              )}
            />
            {errors.password && (
              <Text className="text-state-error text-xs mt-1 ml-1">
                {errors.password.message}
              </Text>
            )}
          </View>

          <Pressable
            onPress={handleSubmit(onSubmit)}
            disabled={isLoading}
            className="p-4 rounded-xl items-center shadow-sm bg-primary"
            style={({ pressed }) => [
              {
                opacity: pressed || isLoading ? 0.8 : 1,
                transform: [{ scale: pressed ? 0.98 : 1 }],
              },
            ]}
          >
            {isLoading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text className="text-white font-bold text-lg">Sign in</Text>
            )}
          </Pressable>

          <View className="mt-8 flex-row justify-center">
            <Text className="text-dark-700 dark:text-text-muted">
              Don't have an account?{" "}
            </Text>
            <Pressable onPress={() => router.push("/(auth)/register")}>
              {({ pressed }) => (
                <Text
                  className={clsx(
                    "font-bold text-primary",
                    pressed && "underline opacity-80"
                  )}
                >
                  Sign up
                </Text>
              )}
            </Pressable>
          </View>

        </ScrollView>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
}

export default Login