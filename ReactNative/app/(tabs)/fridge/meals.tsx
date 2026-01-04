import SearchBar from "@/components/SearchBar";
import MealCard from "@/components/fridge/MealCard";
import React, {useEffect, useMemo, useState} from "react";
import {ActivityIndicator, FlatList, Pressable, Text, View} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import fridgeMealsService, {
  AddMealData,
  IngredientDisplayItem,
  Meal,
  UpdateMealData
} from "@/services/fridgeMealsService";
import Toast from "react-native-toast-message";
import AddMealModal from "@/components/fridge/AddMealModal";
import EditMealModal from "@/components/fridge/EditMealModal";

const FridgeMealsScreen = () => {
  const [searchText, setSearchText] = useState("");
  const [showFavourites, setShowFavourites] = useState(false);
  const [meals, setMeals] = useState<Meal[]>([])
  const [isFetching, setIsFetching] = useState(true);
  const [isAddMealModalVisible, setIsAddMealModalVisible] = useState(false);
  const [selectedMeal, setSelectedMeal] = useState<Meal | null>(null);
  const [isEditMealModalVisible, setIsEditMealModalVisible] = useState(false);

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
      const newMeal = await fridgeMealsService.addMealWithIngredients(newMealData);

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
      await fridgeMealsService.updateMeal(meal.id, {is_favourite: !meal.is_favourite})
      const updatedMeals = meals.map(
        m => m.id === meal.id ? {...m, is_favourite: !m.is_favourite } : m);
      setMeals(updatedMeals);

    } catch (error) {
      console.error(error);
      setMeals(meals);
      Toast.show({
        type: 'error',
        text1: 'Failed to update meal'
      })
    }
  }

  const handleEditMeal = async (data: UpdateMealData) => {
    if (selectedMeal === null) { return;}
    try {
      const newMeal = await fridgeMealsService.updateMeal(selectedMeal.id, {name: data.name});
      const updateMeals = meals.map(
        m => m.id === selectedMeal.id ? newMeal : m);
      setMeals(updateMeals);
      setSelectedMeal(null);
    } catch (error) {
      console.error(error);
      setMeals(meals);
      Toast.show({
        type: 'error',
        text1: 'Failed to update meal'
      })
    }
  }

  const handleEditMealModalClose = async (shouldRefresh?: boolean)=> {
    setIsEditMealModalVisible(false)
    if (shouldRefresh && selectedMeal) {
      const updatedMeal = await fridgeMealsService.getMealById(selectedMeal.id);

      setMeals((prevMeals) =>
        prevMeals.map((m) => m.id === updatedMeal.id ? updatedMeal : m)
      );
    }
  }

  const handleDeleteMeal = async (meal: Meal) => {
    try {
      const response = await fridgeMealsService.deleteMeal(meal.id);
      setMeals( (prevMeals) => prevMeals.filter((m) => m.id !== meal.id));
      Toast.show({
        type: 'success',
        text1: `${response.name} deleted successfully`,
      })

    } catch (error) {
      console.error(error);
      Toast.show({
        type: 'error',
        text1: 'Failed to delete meal',
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
              <Ionicons name="fast-food-outline" size={48} color="gray" opacity={0.5} />
              <Text className="text-gray-400 mt-2">No meals found</Text>
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
              weight={item.weight}
              isFavourite={item.is_favourite}
              onToggleFavourite={() =>  handleToggleFavourite(item)}
              onPress={() => {
                setIsEditMealModalVisible(true);
                setSelectedMeal(item)
              }}
            />
          )}
        />
      )}

      <Pressable
        onPress={() => setIsAddMealModalVisible(true)}
        className="absolute bottom-8 right-8 w-16 h-16 bg-primary rounded-full items-center justify-center shadow-lg shadow-black/30 elevation-5 active:scale-95 transition-transform">
        <Ionicons name="add" size={32} color="white" />
      </Pressable>

      <EditMealModal
        isVisible={isEditMealModalVisible}
        onClose={handleEditMealModalClose}
        onSubmit={handleEditMeal}
        onDelete={handleDeleteMeal}
        meal={selectedMeal}
      />
      <AddMealModal
        isVisible={isAddMealModalVisible}
        onClose={() => setIsAddMealModalVisible(false)}
        onSubmit={handleAddMeal}
      />
    </View>
  );
};

export default FridgeMealsScreen;
