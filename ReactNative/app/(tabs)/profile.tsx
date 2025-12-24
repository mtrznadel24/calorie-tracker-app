import {View, Text, Pressable, ActivityIndicator} from "react-native";
import React from "react";
import {useAuth} from "@/contexts/AuthContext";

const Profile = () => {
  const { logout, isLoading, user } = useAuth();

  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-800 p-6 items-center">
      <View className="mt-10 items-center">
        <View className="w-24 h-24 bg-primary-500 rounded-full items-center justify-center mb-4">
          <Text className="text-white text-3xl font-bold">
             Profile
          </Text>
        </View>
        <Text className="text-dark-800 dark:text-light-100 text-2xl font-bold">
          {user?.username || "Użytkownik"}
        </Text>
        <Text className="text-gray-500 text-base mb-10">
          {user?.email}
        </Text>
      </View>

      <Pressable
        onPress={() => logout()}
        disabled={isLoading}
        className={`w-full max-w-xs h-14 rounded-2xl flex-row items-center justify-center 
          ${isLoading ? "bg-gray-400" : "bg-red-500 active:bg-red-600"}`}
      >
        {isLoading ? (
          <ActivityIndicator color="white" />
        ) : (
          <Text className="text-white font-bold text-lg">Logout</Text>
        )}
      </Pressable>
    </View>
  );
};

export default Profile;