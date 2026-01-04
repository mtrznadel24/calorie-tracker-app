import { View, Text, TextInput, Pressable, KeyboardAvoidingView, Platform, ScrollView } from 'react-native';
import React, { useMemo, useState } from 'react';
import GenderButton from "@/components/profile/GenderButton"; // Zakładam, że to ten komponent z poprzedniej rozmowy
import { useAuth } from "@/contexts/AuthContext";
import { api } from "@/api/axiosInstance";
import Toast from "react-native-toast-message";
import { SafeAreaView } from "react-native-safe-area-context";
import userService, {UserUpdateData} from "@/services/userService";

const Details = () => {
  const { user, setUser } = useAuth();

  const [selectedGender, setSelectedGender] = useState<'male' | 'female' | null>(user?.gender || null);
  const [age, setAge] = useState<string>(user?.age?.toString() || '');
  const [height, setHeight] = useState<string>(user?.height?.toString() || '');

  const [isSaving, setIsSaving] = useState(false);

  const hasChanges = useMemo(() => {
    const currentAge = parseInt(age) || 0;
    const currentHeight = parseFloat(height) || 0;

    const genderChanged = selectedGender !== user?.gender;
    const ageChanged = currentAge !== (user?.age || 0);
    const heightChanged = currentHeight !== (user?.height || 0);

    return (genderChanged || ageChanged || heightChanged) && age !== '' && height !== '';
  }, [age, height, selectedGender, user]);


  const updateProfile = async () => {
    if (!hasChanges || isSaving) return;

    setIsSaving(true);
    try {
      const data: UserUpdateData = {
        age: parseInt(age),
        gender: selectedGender,
        height: parseFloat(height),
      };

      const updatedUser = await userService.updateProfile(data)

      setUser(updatedUser);

      Toast.show({ type: "success", text1: "Profile updated successfully" });
    } catch (error) {
      console.error(error);
      Toast.show({ type: "error", text1: "Failed to update profile" });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      className="flex-1 bg-light-100 dark:bg-dark-800"
    >
      <ScrollView contentContainerStyle={{ padding: 24 }}>

        <View className="mb-8">
          <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-3 ml-1">
            Biological Gender
          </Text>
          <View className="flex-row gap-4">
            <GenderButton label="Male" icon="male" isSelected={selectedGender === 'male'} onPress={() => setSelectedGender('male')} />
            <GenderButton label="Female" icon="female" isSelected={selectedGender === 'female'} onPress={() => setSelectedGender('female')} />
          </View>
        </View>

        <View className="flex-row gap-4 mb-8">

          <View className="flex-1">
            <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-2 ml-1">
              Age
            </Text>
            <View className="bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-2xl px-4 py-3">
              <TextInput
                value={age}
                onChangeText={setAge}
                placeholder="0"
                placeholderTextColor="#9CA3AF"
                keyboardType="numeric"
                className="text-lg font-semibold text-dark-900 dark:text-white"
              />
            </View>
          </View>

          <View className="flex-1">
            <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-2 ml-1">
              Height (cm)
            </Text>
            <View className="bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-2xl px-4 py-3">
              <TextInput
                value={height}
                onChangeText={setHeight}
                placeholder="0"
                placeholderTextColor="#9CA3AF"
                keyboardType="numeric"
                className="text-lg font-semibold text-dark-900 dark:text-white"
              />
            </View>
          </View>

        </View>

        <Pressable
          onPress={updateProfile}
          disabled={!hasChanges || isSaving}
          className={`w-full py-6 rounded-2xl items-center justify-center shadow-sm
            ${hasChanges && !isSaving 
              ? "bg-primary active:opacity-90" 
              : "bg-gray-300 dark:bg-dark-700 opacity-50"
            }`}
        >
          <Text className={`text-lg font-bold ${hasChanges && !isSaving ? "text-white" : "text-gray-500 dark:text-gray-400"}`}>
            {isSaving ? "Saving..." : "Save Changes"}
          </Text>
        </Pressable>

        <Text className="text-center text-gray-400 text-xs mt-8 px-4">
          These details are used to calculate your BMR and daily calorie needs.
        </Text>

      </ScrollView>



    </KeyboardAvoidingView>
  )
}

export default Details