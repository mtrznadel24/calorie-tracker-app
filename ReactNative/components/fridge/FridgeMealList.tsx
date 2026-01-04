import React, { useEffect, useMemo, useState } from "react";
import {
  View,
  Text,
  FlatList,
  Pressable,
  ActivityIndicator,
  RefreshControl
} from "react-native";
import { Meal } from "@/services/fridgeMealsService";
import fridgeMealsService from "@/services/fridgeMealsService";
import { Ionicons } from "@expo/vector-icons";
import SearchBar from "@/components/SearchBar";

interface FridgeMealListProps {
  onMealPress: (meal: Meal) => void;
}

const FridgeMealList = ({ onMealPress }: FridgeMealListProps) => {
  const [meals, setMeals] = useState<Meal[]>([]);
  const [searchText, setSearchText] = useState("");
  const [showFavourites, setShowFavourites] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchMeals = async () => {
    try {
      const data = await fridgeMealsService.getMeals();
      setMeals(data);
    } catch (error) {
      console.error("Failed to fetch meals", error);
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchMeals();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchMeals();
  };

  const filteredMeals = useMemo(() => {
    return meals.filter((item) => {
      const matchesSearch = item.name.toLowerCase().includes(searchText.toLowerCase());
      const matchesFavourite = !showFavourites || item.is_favourite;
      return matchesSearch && matchesFavourite;
    })
  }, [meals, searchText, showFavourites]);

  if (isLoading) {
    return (
      <View className="flex-1 justify-center items-center pt-10">
        <ActivityIndicator size="large" color="#3b82f6" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-900">
      <View className="flex-row items-center gap-3 px-3 py-3">
        <View className="flex-1 h-12">
          <SearchBar
            value={searchText}
            onChangeText={setSearchText}
            placeholder="Search meals"
          />
        </View>
        <Pressable
          onPress={() => setShowFavourites((prev) => !prev)}
          className={`w-12 h-12 rounded-full items-center justify-center border ${
            showFavourites
              ? "bg-red-100 border-red-200 dark:bg-red-900/30 dark:border-red-800"
              : "bg-light-200 border-light-200 dark:bg-dark-600 dark:border-dark-600"
          }`}
        >
          <Ionicons
            name={showFavourites ? "heart" : "heart-outline"}
            size={24}
            color={showFavourites ? "#EF4444" : "#A1A1A1"}
          />
        </Pressable>
      </View>

      <FlatList
        data={filteredMeals}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={{ paddingHorizontal: 16, paddingBottom: 100, paddingTop: 8 }}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View className="items-center justify-center mt-10">
            <Ionicons name="fast-food-outline" size={48} color="gray" opacity={0.5} />
            <Text className="text-gray-400 mt-2">No meals found</Text>
          </View>
        }
        renderItem={({ item }) => (
          <Pressable
            onPress={() => onMealPress(item)}
            className="bg-white dark:bg-dark-800 p-3.5 rounded-2xl mb-3 shadow-sm border border-light-200 dark:border-dark-700 active:bg-gray-50 dark:active:bg-dark-700 flex-row justify-between items-center"
          >
              <View className="flex-1 pr-4 justify-center">
                <Text
                  className="text-base font-bold text-dark-900 dark:text-gray-100 mb-1.5"
                  numberOfLines={1}
                  ellipsizeMode="tail"
                >
                  {item.name}
                </Text>

                <View className="flex-row items-center">
                  <Ionicons name="restaurant-outline" size={12} color="#9CA3AF" style={{ marginRight: 4 }} />
                  <Text className="text-xs text-gray-400 font-medium">
                    {item.products_count} products • {item.weight || 100}g
                  </Text>
                </View>
              </View>

              <View className="items-end justify-center">
                <View className="flex-row items-baseline mb-1">
                  <Text className="text-lg font-extrabold text-primary dark:text-blue-400">
                    {item.calories.toFixed(0)}
                  </Text>
                  <Text className="text-xs text-gray-400 ml-0.5 font-medium">kcal</Text>
                </View>

                <View className="flex-row items-center gap-2">
                  <View className="flex-row items-center bg-blue-50 dark:bg-blue-900/20 px-1.5 py-0.5 rounded-md">
                    <Text className="text-[10px] font-black text-blue-600 dark:text-blue-400 mr-1">P</Text>
                    <Text className="text-[10px] font-bold text-gray-600 dark:text-gray-300">
                      {item.proteins.toFixed(0)}
                    </Text>
                  </View>

                  <View className="flex-row items-center bg-yellow-50 dark:bg-yellow-900/20 px-1.5 py-0.5 rounded-md">
                    <Text className="text-[10px] font-black text-yellow-600 dark:text-yellow-400 mr-1">F</Text>
                    <Text className="text-[10px] font-bold text-gray-600 dark:text-gray-300">
                      {item.fats.toFixed(0)}
                    </Text>
                  </View>

                  <View className="flex-row items-center bg-orange-50 dark:bg-orange-900/20 px-1.5 py-0.5 rounded-md">
                    <Text className="text-[10px] font-black text-orange-600 dark:text-orange-400 mr-1">C</Text>
                    <Text className="text-[10px] font-bold text-gray-600 dark:text-gray-300">
                      {item.carbs.toFixed(0)}
                    </Text>
                  </View>
                </View>
              </View>
          </Pressable>
        )}
      />
    </View>
  );
};

export default FridgeMealList;