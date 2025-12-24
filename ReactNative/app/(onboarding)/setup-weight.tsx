import {
  View,
  Text,
  TouchableWithoutFeedback,
  Keyboard,
  Pressable,
  ActivityIndicator,
  useColorScheme, TextInput
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
import weightService from "@/services/weightService";
import {MaterialCommunityIcons} from "@expo/vector-icons";


const weightSchema = z.object({
  weight: z.preprocess(
    (val) => (val === "" || val === null ? null : Number(val)),
    z.number()
      .min(20, "Weight must be at least 20 kg")
      .max(300, "Enter a realistic weight")
      .nullable()
  ),
});

type WeightForm = z.infer<typeof weightSchema>;

const SetupWeight = () => {
  const { setUser, isLoading } = useAuth();
  const router = useRouter();
  const colorScheme = useColorScheme();

  const { control, handleSubmit, formState: { errors } } = useForm<WeightForm>({
    resolver: zodResolver(weightSchema) as any,
    defaultValues: {
      weight: null
    }
  });

  const onSubmit = async (data: WeightForm) => {
    try {
      await weightService.createWeight(data);
      router.replace("/(onboarding)/setup-activity-level")
    } catch (error) {
      Toast.show({
        type: 'error',
        text1: 'Update Failed',
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
        <View className="p-6 pt-32 flex1">
          <View className="items-center mb-8">
            <View className="w-20 h-20 bg-primary/10 rounded-full items-center justify-center mb-4">
              <MaterialCommunityIcons
                name="scale-bathroom"
                size={45}
                color="#3b82f6"
              />
            </View>
            <Text className="text-2xl font-bold text-dark-900 dark:text-text-light text-center">
              What is your weight? (2/3)
            </Text>
            <Text className="text-sm text-dark-700 dark:text-text-muted text-center mt-2">
              This helps us calculate your daily calorie needs.
            </Text>
          </View>

          <View className="mb-10">
            <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted ml-1">Current Weight (kg)</Text>
            <Controller
              control={control}
              name="weight"
              render={({ field: { onChange, onBlur, value } }) => (
                <View className="relative">
                  <TextInput
                    className={clsx(
                      "p-4 h-16 rounded-2xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light text-xl text-center font-bold",
                      errors.weight ? "border-state-error" : "border-light-300 dark:border-dark-600"
                    )}
                    placeholder="e.g. 75"
                    placeholderTextColor="#9CA3AF"
                    onBlur={onBlur}
                    onChangeText={onChange}
                    value={value ? value.toString() : ""}
                    keyboardType="decimal-pad"
                  />
                </View>
              )}
            />
            {errors.weight && (
              <Text className="text-state-error text-xs mt-2 text-center">
                {errors.weight.message}
              </Text>
            )}
          </View>

          <View className="mt-auto pb-10">
            <Pressable
              onPress={handleSubmit(onSubmit)}
              disabled={isLoading}
              className="p-4 rounded-2xl items-center shadow-sm bg-primary mb-3 h-14 justify-center"
              style={({ pressed }) => [{ opacity: pressed || isLoading ? 0.8 : 1 }]}
            >
              {isLoading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text className="text-white font-bold text-lg">Next Step</Text>
              )}
            </Pressable>

            <Pressable
              onPress={ () => router.replace("/(onboarding)/setup-activity-level")}
              disabled={isLoading}
              className="p-4 rounded-xl items-center"
              style={({ pressed }) => [{ opacity: pressed ? 0.6 : 1 }]}
            >
              <Text className="text-gray-500 dark:text-gray-400 font-semibold text-base underline">
                Skip for now
              </Text>
            </Pressable>
          </View>
        </View>
      </TouchableWithoutFeedback>
    </KeyboardAwareScrollView>
  )
}

export default SetupWeight;