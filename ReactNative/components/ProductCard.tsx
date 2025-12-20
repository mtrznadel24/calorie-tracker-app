import { Ionicons } from "@expo/vector-icons";
import React from 'react';
import { Pressable, Text, View } from 'react-native';

interface ProductProps {
  id: number;
  name: string;
  category: string;
  calories: number;
  proteins: number;
  fats: number;
  carbs: number;
  isFavourite: boolean;
  onPress?: () => void;
  onToggleFavourite?: () => void;
}

const ProductCard = ({ 
  name, 
  category, 
  calories, 
  proteins, 
  fats, 
  carbs, 
  isFavourite,
  onPress,
  onToggleFavourite 
}: ProductProps) => {
  return (
    <Pressable 
      onPress={onPress}
      className="bg-white dark:bg-dark-700 rounded-2xl p-4 mb-3 shadow-sm mx-3 border border-light-200 dark:border-dark-600 active:opacity-70"
    >
      <View className="flex-row justify-between items-start mb-2">
        <View className="flex-1 pr-2">
          <Text 
            className="text-lg font-bold text-text-dark dark:text-text-light"
            numberOfLines={1}
            ellipsizeMode="tail"
          >
            {name}
          </Text>
          <Text className="text-xs text-text-muted capitalize">
            {category} • 100g
          </Text>
        </View>
        
        <Pressable onPress={onToggleFavourite} hitSlop={10}>
          <Ionicons 
            name={isFavourite ? "heart" : "heart-outline"} 
            size={24} 
            color={isFavourite ? "#EF4444" : "#A1A1A1"} 
          />
        </Pressable>
      </View>

      <View className="flex-row items-center justify-between mt-2 pt-3 border-t border-light-200 dark:border-dark-600">
              
        <View>
            <Text className="text-xl font-bold text-primary">
                {calories.toFixed(0)} <Text className="text-xs font-normal text-text-muted">kcal</Text>
            </Text>
        </View>

        <View className="flex-row items-center gap-3">
            <View className="flex-row gap-3 mr-1">
                <View className="items-center">
                    <Text className="text-[10px] font-bold text-blue-600 dark:text-blue-400 mb-0.5">P</Text>
                    <Text className="text-sm font-semibold text-text-dark dark:text-text-light">{proteins.toFixed(0)}</Text>
                </View>
                
                <View className="items-center">
                    <Text className="text-[10px] font-bold text-yellow-500 dark:text-yellow-400 mb-0.5">F</Text>
                    <Text className="text-sm font-semibold text-text-dark dark:text-text-light">{fats.toFixed(0)}</Text>
                </View>
                
                <View className="items-center">
                    <Text className="text-[10px] font-bold text-[#8B4513] dark:text-[#CD853F] mb-0.5">C</Text>
                    <Text className="text-sm font-semibold text-text-dark dark:text-text-light">{carbs.toFixed(0)}</Text>
                </View>
            </View>

            <Ionicons name="chevron-forward" size={18} color="#A1A1A1" />
        </View>

      </View>
    </Pressable>
  );
};

export default ProductCard;