import SearchBar from "@/components/SearchBar";
import MealCard from "@/components/fridge/MealCard";
import React, {useEffect, useMemo, useState} from "react";
import {ActivityIndicator, FlatList, Pressable, Text, View} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import fridgeMealsService, {AddMealData, Meal} from "@/services/fridgeMealsService";
import Toast from "react-native-toast-message";
import AddMealModal from "@/components/fridge/AddMealModal";
import fridgeProductsService, {Product} from "@/services/fridgeProductsService";

const FridgeMealsScreen = () => {
  const [searchText, setSearchText] = useState("");
  const [showFavourites, setShowFavourites] = useState(false);
  const [meals, setMeals] = useState<Meal[]>([])
  const [isFetching, setIsFetching] = useState(true);
  const [isAddMealModalVisible, setIsAddMealModalVisible] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsFetching(true);
        const response = await fridgeMealsService.getMeals();
        setMeals(response);
      } catch (error) {
        console.log(error);
        Toast.show({
        type: 'error',
        text1: 'Fetching data fail',
        text2: 'Something went wrong ❌'
        });
      } finally {
        setIsFetching(false);
      }
    }
    fetchData();
  }, [])

  const filteredMeals = useMemo(() => {
    return meals.filter((item) => {
      const matchesSearch = item.name.toLowerCase().includes(searchText.toLowerCase());
      const matchesFavourite = !showFavourites || item.is_favourite;
      return matchesSearch && matchesFavourite;
    })
  }, [meals, searchText, showFavourites]);

  const handleAddMeal = async (newMealData: AddMealData) => {
    try {
      const newMeal = await fridgeMealsService.addMeal(newMealData);

      setMeals(prevMeals => [...prevMeals, newMeal]);

      Toast.show({
        type: 'success',
        text1: 'Product added!'
      });
    } catch (error) {
      console.log(error);
      Toast.show({ type: 'error', text1: 'Failed to add product' });
    }
  };

  const handleToggleFavourite = async (meal: Meal) => {
    try {
      const updatedMeals = meals.map(
        m => m.id === meal.id ? {...m, is_favourite: !m.is_favourite } : m);
      setMeals(updatedMeals);

      await fridgeMealsService.updateMeal(meal.id, {is_favourite: !meal.is_favourite})
    } catch (error) {
      console.error(error);
      setMeals(meals);
      Toast.show({
        type: 'error',
        text1: 'Failed to update meal'
      })
    }
  }


  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-800 relative">
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

      {isFetching ? (
        <View className="flex-1 justify-center items-center mt-10">
            <ActivityIndicator size="large" color="#3b82f6" />
        </View>
      ) : (
        <FlatList
          data={filteredMeals}
          keyExtractor={(item) => item.id.toString()}
          className="mt-2"
          contentContainerStyle={{ paddingBottom: 100, paddingTop: 10 }}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <View className="items-center justify-center mt-10">
              <Text className="text-gray-400">No meals found</Text>
            </View>
          }
          renderItem={({ item }) => (
            <MealCard
              id={item.id}
              name={item.name}
              calories={item.calories}
              proteins={item.proteins}
              fats={item.fats}
              carbs={item.carbs}
              productsCount={item.products_count}
              isFavourite={item.is_favourite}
              onToggleFavourite={() =>  handleToggleFavourite(item)}
              onPress={() => console.log("Open meal details ID:", item.id)}
            />
          )}
        />
      )}

      <Pressable
        onPress={() => setIsAddMealModalVisible(true)}
        className="absolute bottom-8 right-8 w-16 h-16 bg-primary rounded-full items-center justify-center shadow-lg shadow-black/30 elevation-5 active:scale-95 transition-transform">
        <Ionicons name="add" size={32} color="white" />
      </Pressable>

      <AddMealModal
        isVisible={isAddMealModalVisible}
        onClose={() => setIsAddMealModalVisible(false)}
        onSubmit={handleAddMeal}
      />
    </View>
  );
};

export default FridgeMealsScreen;
