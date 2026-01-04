import { View, Text, Pressable, ActivityIndicator, ScrollView } from "react-native";
import React from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "expo-router";
import { Ionicons } from "@expo/vector-icons";
import { SafeAreaView } from "react-native-safe-area-context";
import MenuButton from "@/components/profile/MenuButton";

const Profile = () => {
  const { logout, isLoading, user } = useAuth();
  const router = useRouter();

  return (
    <SafeAreaView className="flex-1 bg-light-100 dark:bg-dark-900">
      <ScrollView contentContainerStyle={{ padding: 24 }}>
        <View className="items-center mt-4 mb-8">
          <View className="w-24 h-24 bg-blue-500 rounded-full items-center justify-center mb-4 shadow-xl">
             <Text className="text-white text-3xl font-black">
                {user?.username?.charAt(0).toUpperCase()}
             </Text>
          </View>
          <Text className="text-dark-900 dark:text-light-100 text-2xl font-black tracking-tight">
            Hello, {user?.username}!
          </Text>
          <Text className="text-gray-500 dark:text-gray-400 font-medium">
            {user?.email}
          </Text>
        </View>

        <View className="mb-8">
          <MenuButton
            title="Personal Info"
            icon="person-outline"
            onPress={() => router.push("/profile/details")}
            color="#3b82f6"
          />
          <MenuButton
            title="Body & Goals"
            icon="fitness-outline"
            onPress={() => router.push("/profile/goals")}
            color="#10b981"
          />
          <MenuButton
            title="Measurements"
            icon="stats-chart-outline"
            onPress={() => router.push("/profile/measurements")}
            color="#8b5cf6"
          />
          <MenuButton
            title="Account Settings"
            icon="settings-outline"
            onPress={() => router.push("/profile/security")}
            color="#f59e0b"
          />
        </View>

        <Pressable
          onPress={() => logout()}
          disabled={isLoading}
          className={`w-full h-14 rounded-2xl flex-row items-center justify-center shadow-sm
            ${isLoading ? "bg-gray-300 dark:bg-dark-600" : "bg-red-50 dark:bg-red-900/20 active:bg-red-100"}`}
        >
          {isLoading ? (
            <ActivityIndicator color="#ef4444" />
          ) : (
            <>
              <Ionicons name="log-out-outline" size={22} color="#ef4444" className="mr-2" />
              <Text className="text-red-500 font-bold text-lg ml-2">Logout</Text>
            </>
          )}
        </Pressable>

        <Text className="text-center text-gray-400 dark:text-gray-600 mt-8 text-xs font-medium">
          App Version 1.0.0
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
};

export default Profile;