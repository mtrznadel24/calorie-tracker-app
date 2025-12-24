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
import React from 'react';
import { z } from "zod";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "expo-router";
import {Controller, useForm} from "react-hook-form";
import Toast from "react-native-toast-message";
import clsx from "clsx";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";
import {zodResolver} from "@hookform/resolvers/zod";
import userService from "@/services/userService";
import {MaterialCommunityIcons} from "@expo/vector-icons";



const activityLevelSchema = z.object({
  activityLevel: z.preprocess(
    (val) => (val === "" || val === null ? null : Number(val)),
    z.number()
      .min(1, "activity level cannot be less than 0")
      .max(5, "activity level too high")
      .nullable()
  ),
});

type ActivityLevelForm = z.infer<typeof activityLevelSchema>;

const ACTIVITY_LEVELS = [
  { id: 1.2, label: "Sedentary", desc: "Little or no exercise, desk job", icon: "chair-school" },
  { id: 1.375, label: "Lightly Active", desc: "Light exercise 1-3 days/week", icon: "walk" },
  { id: 1.55, label: "Moderately Active", desc: "Moderate exercise 3-5 days/week", icon: "run" },
  { id: 1.725, label: "Very Active", desc: "Hard exercise 6-7 days/week", icon: "bike" },
  { id: 1.9, label: "Extra Active", desc: "Very hard exercise, physical job", icon: "fire" },
];

const SetupActivityLevel = () => {
  const { setUser, isLoading } = useAuth();
  const router = useRouter();
  const colorScheme = useColorScheme();

  const { control, handleSubmit, watch, formState: { errors } } = useForm<ActivityLevelForm>({
    resolver: zodResolver(activityLevelSchema) as any,
    defaultValues: {
      activityLevel: 1.2
    }
  });

  const selectedLevel = watch("activityLevel");

  const onSubmit = async (data: ActivityLevelForm) => {
    try {
      const payload = { activity_level: data.activityLevel };
      const updatedUser = await userService.updateProfile(payload);
      setUser(updatedUser);
      router.replace("/(tabs)/meals");
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Update Failed'
      });
    }
  };

  const onSkip = async () => {
    try {
      router.replace("/(tabs)/meals")
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Something went wrong ❌'
      });
    }
  }

  return (
    <KeyboardAwareScrollView contentContainerStyle={{ flexGrow: 1 }} className="bg-light-50 dark:bg-dark-900">
      <View className="p-6 pt-20">
        <Text className="text-2xl font-bold text-dark-900 dark:text-text-light mb-2 text-center">
          What is your activity level? (3/3)
        </Text>
        <Text className="text-sm text-dark-700 dark:text-text-muted mb-8 text-center">
          This is used to calculate your maintenance calories.
        </Text>

        <Controller
          control={control}
          name="activityLevel"
          render={({ field: { onChange } }) => (
            <View className="gap-y-3">
              {ACTIVITY_LEVELS.map((level) => (
                <Pressable
                  key={level.id}
                  onPress={() => onChange(level.id)}
                  className={clsx(
                    "flex-row items-center p-4 rounded-2xl border-2 transition-all",
                    selectedLevel === level.id
                      ? "border-primary bg-primary/5 dark:bg-primary/10"
                      : "border-light-200 dark:border-dark-700 bg-light-100 dark:bg-dark-800"
                  )}
                >
                  <View className={clsx(
                    "w-12 h-12 rounded-full items-center justify-center mr-4",
                    selectedLevel === level.id ? "bg-primary" : "bg-light-300 dark:bg-dark-600"
                  )}>
                    <MaterialCommunityIcons
                      name={level.icon as any}
                      size={24}
                      color={selectedLevel === level.id ? "white" : "#9CA3AF"}
                    />
                  </View>

                  <View className="flex-1">
                    <Text className={clsx(
                      "font-bold text-lg",
                      selectedLevel === level.id ? "text-primary" : "text-dark-900 dark:text-text-light"
                    )}>
                      {level.label}
                    </Text>
                    <Text className="text-xs text-dark-600 dark:text-text-muted">
                      {level.desc}
                    </Text>
                  </View>

                  {selectedLevel === level.id && (
                    <MaterialCommunityIcons name="check-circle" size={24} color="#3b82f6" />
                  )}
                </Pressable>
              ))}
            </View>
          )}
        />

        <View className="mt-10">
          <Pressable
            onPress={handleSubmit(onSubmit)}
            disabled={isLoading}
            className="p-4 rounded-2xl items-center shadow-sm bg-primary mb-3 h-14 justify-center"
          >
            {isLoading ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-bold text-lg">Finish & Start</Text>}
          </Pressable>

          <Pressable onPress={() => router.replace("/(tabs)/meals")} className="p-4 items-center">
            <Text className="text-gray-500 dark:text-gray-400 font-semibold underline">Skip</Text>
          </Pressable>
        </View>
      </View>
    </KeyboardAwareScrollView>
  );
};

export default SetupActivityLevel;