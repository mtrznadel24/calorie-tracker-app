import {View, Text, ActivityIndicator, SectionList, Pressable} from "react-native";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import mealService, {
  formatDateForApi, FromMealAddLogData, FromProductAddLogData,
  MealLog,
  QuickAddLogData,
  SimpleProductData
} from "@/services/mealService";
import Toast from "react-native-toast-message";
import {SafeAreaView} from "react-native-safe-area-context";
import {Ionicons} from "@expo/vector-icons";
import AddMealLogModal from "@/components/meals/AddMealLogModal";
import {Product} from "@/services/fridgeProductsService";
import {Meal} from "@/services/fridgeMealsService";
import {useFocusEffect} from "expo-router";
import LogModal from "@/components/meals/LogModal";
import {useAuth} from "@/contexts/AuthContext";

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
  const [isAddMealLogModalOpen, setIsAddMealLogModalOpen] = useState(false);
  const [isLogModalOpen, setIsLogModalOpen] = useState(false);
  const [selectedSection, setSelectedSection] = useState<string | null>(null);
  const [selectedLog, setSelectedLog] = useState<MealLog | null>(null);
  const { user } = useAuth();


  useFocusEffect(
    useCallback(() => {
      const today = new Date();
      setDate(today);
      fetchMealLogs(today);
    }, [])
  );

  const fetchMealLogs = async (selectedDate = date) => {
      setIsLoading(true);
      try {
        const logs = await mealService.getMealLogs(selectedDate);
        setMealLogs(logs);
      } catch (error) {
        console.log(error)
        Toast.show({ type: "error", text1: "Failed to fetch meal logs" });
      } finally {
        setIsLoading(false);
      }
    };

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

  const caloriesGoal = useMemo(() => {

    if (!user || !user.current_weight || !user.height || !user.age || !user.activity_level || !user.gender) {
      return 0;
    }

    let bmr = 0;
    if (user.gender === "male") {
      bmr = (10 * user.current_weight) + (6.25 * user.height) - (5 * user.age) + 5
    } else if (user.gender === "female") {
      bmr = (10 * user.current_weight) + (6.25 * user.height) - (5 * user.age) - 161
    }
    const tdee = bmr * user.activity_level;
    const surplus = (user.target_weekly_gain || 0) * 1100;

    return Math.round(tdee + surplus);
  }, [user, mealLogs])

  const remainingCalories = useMemo(() => {
    return caloriesGoal - dailyTotals.calories;
  }, [caloriesGoal, dailyTotals.calories]);

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
    fetchMealLogs(newDate);
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
        setIsAddMealLogModalOpen(false);
        setSelectedSection(null);
        Toast.show({ type: "success", text1: "Meal log added successfully." });
      } catch (error) {
        console.error(error);
        Toast.show({ type: "error", text1: "Failed to add log" });
      }
    }

  const handleProductAdd = async (product: Product, weight: number) => {
    if (!selectedSection) { return;}
    try {
      const LogData: FromProductAddLogData = {
        fridge_product_id: product.id,
        date: formatDateForApi(date),
        type: selectedSection,
        weight: weight
      }
      const newLog = await mealService.fromProductCreateMealLog(LogData)
      setMealLogs(prevLogs => [...prevLogs, newLog]);
      setIsAddMealLogModalOpen(false);
      setSelectedSection(null);
      Toast.show({ type: "success", text1: "Meal log added successfully." });
    } catch (error) {
      console.error(error);
      Toast.show({ type: "error", text1: "Failed to add log" });
      }
  }

  const handleAddMealLog = async (meal: Meal, weight: number) => {
    if (!selectedSection) { return;}
    try {
      const LogData: FromMealAddLogData = {
        fridge_meal_id: meal.id,
        date: formatDateForApi(date),
        type: selectedSection,
        weight: weight
      }
      const newLogs = await mealService.fromMealCreateMealLog(LogData);
      setMealLogs(prevLogs => [...prevLogs, ...newLogs]);
      setIsAddMealLogModalOpen(false);
      setSelectedSection(null);
      Toast.show({ type: "success", text1: "Meal logs added successfully." });
    } catch (error) {
      console.error(error);
      Toast.show({ type: "error", text1: "Failed to add logs" });
    }
  }

  const handleUpdateMealLog = async (name: string, weight: number) => {
    if (!selectedLog) { return;}
    try {
      if (selectedLog.name !== name) {
        const newLog = await mealService.updateMeaLogName(selectedLog.id, name)
        setMealLogs((logs) => logs.map(log => selectedLog.id === log.id ? newLog : log));
      }
      if (selectedLog.weight !== weight) {
        const newLog = await mealService.updateMeaLogWeight(selectedLog.id, weight);
        setMealLogs(logs => logs.map(log => selectedLog.id === log.id ? newLog : log));
      }
      setIsLogModalOpen(false);
      setSelectedLog(null);
      Toast.show({ type: "success", text1: "Updated log successfully." });
    } catch (error) {
      console.error(error);
      Toast.show({ type: "error", text1: "Failed to update log" });
    }
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
                        {sectionCals.toFixed(0)} kcal
                      </Text>
                    </View>
                    <Pressable
                      onPress={() => {
                        setIsAddMealLogModalOpen(true);
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
              <Pressable
                onPress={() => {
                  setSelectedLog(item);
                  setIsLogModalOpen(true);
                }}
                className="bg-white dark:bg-dark-800 p-3.5 rounded-2xl mb-2.5 shadow-sm border border-light-200 dark:border-dark-700 flex-row justify-between items-center active:opacity-70 active:bg-gray-50 dark:active:bg-dark-700">

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

                <View className="items-center flex-col">
                  <View className="flex-row items-baseline">
                    <Text className="text-3xl font-extrabold text-primary tracking-tight">
                      {dailyTotals.calories.toFixed(0)}
                    </Text>
                    <Text className="text-lg text-gray-400 font-medium ml-1">
                      / {caloriesGoal > 0 ? caloriesGoal : '--'}
                    </Text>
                    <Text className="text-xs text-gray-500 font-medium ml-1 mb-2 text-uppercase">kcal</Text>
                  </View>

                  <View className="flex-row items-center mt-[-4]">
                    <Text className="text-xs font-bold text-gray-400 uppercase tracking-tighter">
                      {remainingCalories >= 0 ? 'Remaining: ' : 'Over limit: '}
                    </Text>
                    <Text
                      className={`text-sm font-black ${remainingCalories >= 0 ? 'text-green-700' : 'text-red-500'}`}
                    >
                      {Math.abs(remainingCalories).toFixed(0)}
                    </Text>
                  </View>
                </View>
            </View>

        </View>
      </View>
      <AddMealLogModal
        isVisible={isAddMealLogModalOpen}
        onClose={() => {
          setIsAddMealLogModalOpen(false);
          setSelectedSection(null);
        }}
        onQuickSubmit={handleQuickAddLog}
        onProductSubmit={handleProductAdd}
        onMealSubmit={handleAddMealLog}
        sectionTitle={selectedSection}
      />
      <LogModal
        isVisible={isLogModalOpen}
        onClose={() => {
          setIsLogModalOpen(false);
          setSelectedLog(null);
        }}
        onSubmit={handleUpdateMealLog}
        log={selectedLog}
      />

    </SafeAreaView>
  );
};

export default Meals;