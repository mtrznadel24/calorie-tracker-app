import React from "react";
import { Pressable, View, Text } from "react-native";
import { Ionicons } from "@expo/vector-icons";

interface MenuButtonProps {
  title: string;
  icon: keyof typeof Ionicons.glyphMap;
  onPress: () => void;
  color?: string;
}

const MenuButton = ({ title, icon, onPress, color = "#3b82f6" }: MenuButtonProps) => {
  return (
    <Pressable
      onPress={onPress}
      className="flex-row items-center bg-white dark:bg-dark-700 p-4 rounded-2xl mb-3 border border-light-200 dark:border-dark-600 active:opacity-70 shadow-sm"
    >
      <View
        className="w-10 h-10 rounded-full items-center justify-center"
        style={{ backgroundColor: `${color}20` }}
      >
        <Ionicons name={icon} size={22} color={color} />
      </View>
      <Text className="flex-1 ml-4 text-dark-900 dark:text-light-100 font-semibold text-base">
        {title}
      </Text>
      <Ionicons name={icon ? "chevron-forward" : undefined} size={20} color="#9CA3AF" />
    </Pressable>
  );
};

export default MenuButton;