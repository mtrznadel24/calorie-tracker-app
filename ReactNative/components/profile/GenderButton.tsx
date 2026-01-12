import {Pressable, Text} from "react-native";
import {Ionicons} from "@expo/vector-icons";
import React, {useState} from "react";

interface SelectionProps {
  label: string,
  icon: any,
  isSelected: boolean,
  onPress: () => void,
}

const GenderButton = ({ label, icon, isSelected, onPress }: SelectionProps) => {

  return (
    <Pressable
      onPress={onPress}
      className={`flex-1 flex-row items-center justify-center p-4 rounded-2xl border-2 gap-2 ${
        isSelected 
          ? 'bg-blue-50 border-blue-500 dark:bg-blue-900/20' 
          : 'bg-white border-gray-500 dark:bg-dark-800'
      }`}
    >
      <Ionicons
        name={icon}
        size={20}
        color={isSelected ? '#3b82f6' : '#9CA3AF'}
      />
      <Text className={`font-bold ${
        isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-gray-500'
      }`}>
        {label}
      </Text>
    </Pressable>
  );
};

export default GenderButton;