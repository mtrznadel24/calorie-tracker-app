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


const updateSchema = z.object({
  height: z.preprocess(
    (val) => (val === "" || val === null ? null : Number(val)),
    z.number().min(50, "Enter correct value").max(300, "Enter correct value").nullable()
  ),
  age: z.preprocess(
    (val) => (val === "" || val === null ? null : Number(val)),
    z.number().min(1, "Enter correct value").max(120, "Enter correct value").nullable()
  ),
  gender: z.enum(["male", "female"]).nullable(),
});

type UpdateForm = z.infer<typeof updateSchema>;

const SetupProfile = () => {
  const { setUser, isLoading } = useAuth();
  const router = useRouter();
  const colorScheme = useColorScheme();

  const { control, handleSubmit, formState: { errors } } = useForm<UpdateForm>({
    resolver: zodResolver(updateSchema) as any,
    defaultValues: {
      height: null,
      age: null,
      gender: null
    }
  });

  const onSubmit = async (data: UpdateForm) => {
    try {
      const updatedUser = await userService.updateProfile(data);
      setUser(updatedUser);
      router.replace("/(onboarding)/setup-weight")
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
        <View className="p-6 pt-32">
          <View className="flex">
            <Text className="text-2xl font-bold mb-4 text-dark-900 dark:text-text-light">Personal Details (1/3)</Text>
            <Text className="text-sm text-dark-700 dark:text-text-muted mb-6">Tell us a bit more about yourself.</Text>

            {/* HEIGHT INPUT */}
            <View className="mb-4">
              <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Height (cm)</Text>
              <Controller
                control={control}
                name="height"
                render={({ field: { onChange, onBlur, value } }) => (
                  <TextInput
                    className={clsx("p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light", errors.height ? "border-state-error" : "border-light-300 dark:border-dark-600")}
                    placeholder="e.g. 180"
                    placeholderTextColor="#9CA3AF"
                    onBlur={onBlur}
                    onChangeText={onChange}
                    value={value ? value.toString() : ""}
                    keyboardType="numeric"
                  />
                )}
              />
              {errors.height && <Text className="text-state-error text-xs mt-1 ml-1">{errors.height.message}</Text>}
            </View>

            {/* AGE INPUT */}
            <View className="mb-4">
              <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Age</Text>
              <Controller
                control={control}
                name="age"
                render={({ field: { onChange, onBlur, value } }) => (
                  <TextInput
                    className={clsx("p-4 rounded-xl border bg-light-100 dark:bg-dark-800 text-dark-900 dark:text-text-light", errors.age ? "border-state-error" : "border-light-300 dark:border-dark-600")}
                    placeholder="e.g. 25"
                    placeholderTextColor="#9CA3AF"
                    onBlur={onBlur}
                    onChangeText={onChange}
                    value={value ? value.toString() : ""}
                    keyboardType="numeric"
                  />
                )}
              />
              {errors.age && <Text className="text-state-error text-xs mt-1 ml-1">{errors.age.message}</Text>}
            </View>

            {/* GENDER SELECTION */}
            <View className="mb-6">
              <Text className="mb-3 font-semibold text-dark-700 dark:text-text-muted">Gender</Text>
              <Controller
                control={control}
                name="gender"
                render={({ field: { onChange, value } }) => (
                  <View className="flex-row gap-4">
                    <Pressable
                      onPress={() => onChange("male")}
                      className={clsx("flex-1 p-4 rounded-xl border items-center justify-center", value === "male" ? "bg-primary border-primary" : "bg-light-100 dark:bg-dark-800 border-light-300 dark:border-dark-600")}
                    >
                      <Text className={clsx("font-bold", value === "male" ? "text-white" : "text-dark-700 dark:text-text-muted")}>Male</Text>
                    </Pressable>

                    <Pressable
                      onPress={() => onChange("female")}
                      className={clsx("flex-1 p-4 rounded-xl border items-center justify-center", value === "female" ? "bg-primary border-primary" : "bg-light-100 dark:bg-dark-800 border-light-300 dark:border-dark-600")}
                    >
                      <Text className={clsx("font-bold", value === "female" ? "text-white" : "text-dark-700 dark:text-text-muted")}>Female</Text>
                    </Pressable>
                  </View>
                )}
              />
              {errors.gender && <Text className="text-state-error text-xs mt-2 ml-1">{errors.gender.message}</Text>}
            </View>

            <Pressable
              onPress={handleSubmit(onSubmit)}
              disabled={isLoading}
              className="p-4 rounded-xl items-center shadow-sm bg-primary mb-3"
              style={({ pressed }) => [{ opacity: pressed || isLoading ? 0.8 : 1 }]}
            >
              {isLoading ? <ActivityIndicator color="#fff" /> : <Text className="text-white font-bold text-lg">Next</Text>}
            </Pressable>

            <Pressable
              onPress={ () => router.replace("/(onboarding)/setup-weight")}
              disabled={isLoading}
              className="p-4 rounded-xl items-center mt-2"
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

export default SetupProfile;