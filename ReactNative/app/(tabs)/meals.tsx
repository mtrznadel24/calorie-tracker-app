import {View, Text, ActivityIndicator, SectionList, Pressable} from "react-native";
import React, {useEffect, useMemo, useState} from "react";
import mealService, {
  formatDateForApi,
  MealLog,
  QuickAddLogData,
  SimpleProductData
} from "@/services/mealService";
import Toast from "react-native-toast-message";
import {SafeAreaView} from "react-native-safe-area-context";
import {Ionicons} from "@expo/vector-icons";
import AddMealLogModal from "@/components/meals/AddMealLogModal";
import {Product} from "@/services/fridgeProductsService";

const MEAL_SECTIONS = [
  { title: "Breakfast", type: "breakfast" },
  { title: "Lunch", type: "lunch" },
  { title: "Dinner", type: "dinner" },
  { title: "Snacks", type: "snack" },
  { title: "Supper", type: "supper" }
];

const Meals = () => {
  const [mealLogs, setMealLogs] = useState<MealLog[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [date, setDate] = useState(new Date());
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedSection, setSelectedSection] = useState<string | null>(null);

  useEffect(() => {
    const fetchMealLogs = async () => {
      setIsLoading(true);
      try {
        const logs = await mealService.getMealLogs(date);
        setMealLogs(logs);

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
      type: section.type,
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

    const handleQuickAddLog = async (log: SimpleProductData) => {
      if (!selectedSection) { return;}
      try {
        const logData: QuickAddLogData = {
          name: log.name,
          date: formatDateForApi(date),
          type: selectedSection,
          weight: log.weight,
          calories: Math.round((log.calories_100g * log.weight) / 100),
          proteins: Number(((log.proteins_100g * log.weight) / 100).toFixed(1)),
          fats: Number(((log.fats_100g * log.weight) / 100).toFixed(1)),
          carbs: Number(((log.carbs_100g * log.weight) / 100).toFixed(1)),
        }
        const newLog = await mealService.quickCreateMealLog(logData);
        setMealLogs(prevLogs => [...prevLogs, newLog]);
        setIsModalOpen(false);
        setSelectedSection(null);
      } catch (error) {
        console.error(error);
        Toast.show({ type: "error", text1: "Failed to add log" });
      }
    }

  const handleProductAdd = async (product: Product) => {

  }

  const handleAddMealLog = async () => {

  }

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

            renderSectionHeader={({ section: { title, type, data } }) => {
              const sectionCals = data.reduce((sum, item) => sum + item.calories, 0);

              return (
                <View className="mb-3 mt-6  px-2 py-2">
                  <View className="flex-row justify-between items-end ">
                    <View>
                      <Text className="text-2xl font-bold text-dark-900 dark:text-white tracking-tight">
                      {title}
                      </Text>
                      <Text className="text-sm font-medium text-gray-400 mb-1">
                        {sectionCals} kcal
                      </Text>
                    </View>
                    <Pressable
                      onPress={() => {
                        setIsModalOpen(true);
                        setSelectedSection(type);
                      }}
                      className={"bg-blue-50 dark:bg-blue-900/20 p-2 rounded-full active:bg-blue-100 dark:active:bg-blue-900/40"}
                    >
                      <Ionicons name="add" size={30} color="#3b82f6"/>
                    </Pressable>

                  </View>
                  <View className="h-[1px] w-full bg-gray-200 dark:bg-dark-600 mt-4" />
                </View>
              );
            }}

            renderItem={({ item }) => (
              <View className="bg-white dark:bg-dark-800 p-3.5 rounded-2xl mb-2.5 shadow-sm border border-light-200 dark:border-dark-700 flex-row justify-between items-center">

                <View className="flex-1 pr-4 justify-center">
                  <Text
                    className="text-base font-semibold text-dark-900 dark:text-gray-100 mb-1"
                    numberOfLines={1}
                    ellipsizeMode="tail"
                  >
                    {item.name}
                  </Text>
                  <Text className="text-xs text-gray-400 font-medium">
                    {item.weight}g
                  </Text>
                </View>

                <View className="items-end justify-center">

                  <View className="flex-row items-baseline mb-1">
                    <Text className="text-base font-extrabold text-primary dark:text-blue-400">
                      {item.calories.toFixed(0)}
                    </Text>
                    <Text className="text-[10px] text-gray-400 ml-0.5">kcal</Text>
                  </View>

                  <View className="flex-row items-center gap-3">

                    <View className="flex-row items-center">
                      <Text className="text-[10px] font-black text-blue-600 dark:text-blue-400 mr-1">P</Text>
                      <Text className="text-xs font-semibold text-gray-600 dark:text-gray-300">
                        {item.proteins.toFixed(0)}
                      </Text>
                    </View>

                    <View className="flex-row items-center">
                      <Text className="text-[10px] font-black text-yellow-600 dark:text-yellow-400 mr-1">F</Text>
                      <Text className="text-xs font-semibold text-gray-600 dark:text-gray-300">
                        {item.fats.toFixed(0)}
                      </Text>
                    </View>

                    <View className="flex-row items-center">
                      <Text className="text-[10px] font-black text-orange-600 dark:text-orange-400 mr-1">C</Text>
                      <Text className="text-xs font-semibold text-gray-600 dark:text-gray-300">
                        {item.carbs.toFixed(0)}
                      </Text>
                    </View>

                  </View>
                </View>
              </View>
            )}
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
      <AddMealLogModal
        isVisible={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onQuickSubmit={handleQuickAddLog}
        onProductSubmit={handleProductAdd}
        onMealSubmit={handleAddMealLog}
        sectionTitle={selectedSection}
      />
    </SafeAreaView>
  );
};

export default Meals;