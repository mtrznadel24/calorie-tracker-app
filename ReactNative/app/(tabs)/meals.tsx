import {View, Text, ActivityIndicator, SectionList, Pressable} from "react-native";
import React, {useEffect, useMemo, useState} from "react";
import mealService, {MealLog} from "@/services/mealService";
import Toast from "react-native-toast-message";
import {SafeAreaView} from "react-native-safe-area-context";
import {Ionicons} from "@expo/vector-icons";

const DUMMY_LOGS: MealLog[] = [
  { id: 1, name: "Oatmeal with berries", type: "breakfast", calories: 350, proteins: 12, fats: 6, carbs: 60, weight: 250 },
  { id: 2, name: "Black Coffee", type: "breakfast", calories: 5, proteins: 0, fats: 0, carbs: 1, weight: 200 },
  { id: 3, name: "Grilled Chicken Breast", type: "lunch", calories: 165, proteins: 31, fats: 3.6, carbs: 0, weight: 100 },
  { id: 4, name: "Basmati Rice", type: "lunch", calories: 130, proteins: 2.7, fats: 0.3, carbs: 28, weight: 100 },
  { id: 5, name: "Greek Yoghurt", type: "snack", calories: 120, proteins: 10, fats: 0, carbs: 4, weight: 150 },
];

const MEAL_SECTIONS = [
  { title: "Breakfast", type: "breakfast" },
  { title: "Lunch", type: "lunch" },
  { title: "Dinner", type: "dinner" },
  { title: "Snacks", type: "snack" },
  { title: "Supper", type: "supper" }
];

const Meals = () => {
  const [mealLogs, setMealLogs] = useState<MealLog[]>(DUMMY_LOGS);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [date, setDate] = useState(new Date());

  useEffect(() => {
    const fetchMealLogs = async () => {
      // setIsLoading(true);
      try {
        // const logs = await mealService.getMealLogs(date);
        // setMealLogs(logs);

        setTimeout(() => setMealLogs(DUMMY_LOGS), 500);

      } catch (error) {
        console.error(error);
        Toast.show({ type: "error", text1: "Failed to fetch meal logs" });
      } finally {
        setIsLoading(false);
      }
    };
    fetchMealLogs();
  }, [date]);

  const sections = useMemo(() => {
    return MEAL_SECTIONS.map((section) => ({
      title: section.title,
      data: mealLogs.filter((log) => log.type === section.type),
    }));
  }, [mealLogs]);

  const dailyTotals = useMemo(() => {
    return mealLogs.reduce(
      (acc, curr) => ({
        calories: acc.calories + curr.calories,
        proteins: acc.proteins + curr.proteins,
        fats: acc.fats + curr.fats,
        carbs: acc.carbs + curr.carbs,
      }),
      { calories: 0, proteins: 0, fats: 0, carbs: 0 }
    );
  }, [mealLogs]);

  const formatDate = (d: Date) => {
    return d.toLocaleDateString('en-US', {
      weekday: 'long',
      day: 'numeric',
      month: 'short'
    });
  };

  const changeDate = (days: number) => {
    const newDate = new Date(date);
    newDate.setDate(newDate.getDate() + days);
    setDate(newDate);
  };

  return (
    <SafeAreaView className="flex-1 bg-light-100 dark:bg-dark-900" edges={['top']}>
      <View className="flex-row justify-between items-center px-6 py-4 bg-light-100 dark:bg-dark-900 border-b border-light-200 dark:border-dark-800">
        <Pressable
          onPress={() => changeDate(-1)}
          className="p-2 active:opacity-50"
        >
          <Ionicons name="chevron-back" size={24} color="#9CA3AF" />
        </Pressable>

        <View className="items-center">
          <Text className="text-gray-400 text-xs font-bold uppercase tracking-widest mb-1">
            Selected Day
          </Text>
          <Text className="text-dark-900 dark:text-white text-lg font-bold">
            {formatDate(date)}
          </Text>
        </View>

        <Pressable
          onPress={() => changeDate(1)}
          className="p-2 active:opacity-50"
        >
          <Ionicons name="chevron-forward" size={24} color="#9CA3AF" />
        </Pressable>
      </View>

      <View className="flex-1">
        {isLoading ? (
          <View className="flex-1 justify-center items-center">
             <ActivityIndicator size="large" color="#3b82f6" />
          </View>
        ) : (
          <SectionList
            sections={sections}
            keyExtractor={(item) => item.id.toString()}
            contentContainerStyle={{ paddingBottom: 120, paddingTop: 10, paddingHorizontal: 16 }}
            stickySectionHeadersEnabled={false}

            renderSectionHeader={({ section: { title, data } }) => {
              const sectionCals = data.reduce((sum, item) => sum + item.calories, 0);

              return (
                <View className="flex-row justify-between items-end mt-6 mb-3 px-2">
                  <Text className="text-2xl font-bold text-dark-900 dark:text-white tracking-tight">
                    {title}
                  </Text>
                  <Text className="text-sm font-medium text-gray-400 mb-1">
                    {sectionCals} kcal
                  </Text>
                </View>
              );
            }}

            renderItem={({ item }) => (
              <View className="bg-white dark:bg-dark-800 p-4 rounded-2xl mb-3 shadow-sm border border-light-200 dark:border-dark-700 flex-row justify-between items-center">
                <View className="flex-1 pr-4">
                    <Text className="text-base font-semibold text-dark-900 dark:text-gray-100 mb-1">
                        {item.name}
                    </Text>
                    <Text className="text-xs text-gray-500 font-medium">
                        {item.weight}g
                    </Text>
                </View>

                <View className="items-end">
                    <Text className="text-base font-bold text-primary dark:text-blue-400">
                        {item.calories}
                    </Text>
                    <Text className="text-[10px] text-gray-400">kcal</Text>
                </View>
              </View>
            )}

            ListEmptyComponent={
                <View className="mt-20 items-center">
                    <Text className="text-gray-400 text-lg">No meals logged today</Text>
                </View>
            }
          />
        )}
      </View>

      <View className="absolute bottom-0 left-0 right-0">
        <View className="bg-white dark:bg-dark-800 px-6 py-5 rounded-t-3xl shadow-[0_-5px_20px_rgba(0,0,0,0.05)] border-t border-light-200 dark:border-dark-700">

            <View className="flex-row items-center justify-between">

                <View className="flex-row gap-6">
                    <View>
                        <Text className="text-xs text-gray-400 font-bold mb-0.5">PROTEINS</Text>
                        <Text className="text-lg font-bold text-dark-900 dark:text-white">
                            {dailyTotals.proteins.toFixed(0)}<Text className="text-xs font-normal text-gray-400">g</Text>
                        </Text>
                    </View>
                    <View>
                        <Text className="text-xs text-gray-400 font-bold mb-0.5">CARBS</Text>
                        <Text className="text-lg font-bold text-dark-900 dark:text-white">
                            {dailyTotals.carbs.toFixed(0)}<Text className="text-xs font-normal text-gray-400">g</Text>
                        </Text>
                    </View>
                    <View>
                        <Text className="text-xs text-gray-400 font-bold mb-0.5">FATS</Text>
                        <Text className="text-lg font-bold text-dark-900 dark:text-white">
                            {dailyTotals.fats.toFixed(0)}<Text className="text-xs font-normal text-gray-400">g</Text>
                        </Text>
                    </View>
                </View>

                <View className="items-end">
                    <View className="flex-row items-baseline">
                        <Text className="text-4xl font-extrabold text-primary tracking-tight">
                            {dailyTotals.calories.toFixed(0)}
                        </Text>
                        <Text className="text-sm text-gray-500 font-medium ml-1 mb-1">kcal</Text>
                    </View>
                </View>
            </View>

        </View>
      </View>
    </SafeAreaView>
  );
};

export default Meals;