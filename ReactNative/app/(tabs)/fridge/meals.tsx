import SearchBar from "@/components/SearchBar";
import MealCard from "@/components/fridge/MealCard";
import React, { useState } from "react";
import { FlatList, Pressable, View } from "react-native";
import { Ionicons } from "@expo/vector-icons";

const FridgeMealsScreen = () => {
  const [searchText, setSearchText] = useState("");
  const [showFavourites, setShowFavourites] = useState(false);
  const [meals, setMeals] = useState([])

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

      <FlatList
        data={meals}
        keyExtractor={(item) => item.id.toString()}
        className="mt-2"
        contentContainerStyle={{ paddingBottom: 100, paddingTop: 10 }}
        showsVerticalScrollIndicator={false}
        renderItem={({ item }) => (
          <MealCard
            id={item.id}
            name={item.name}
            calories={item.calories}
            proteins={item.proteins}
            fats={item.fats}
            carbs={item.carbs}
            productsCount={item.count}
            isFavourite={item.isFavourite}
            onToggleFavourite={() =>
              console.log("Clicked heart icon ID:", item.id)
            }
            onPress={() => console.log("Open meal details ID:", item.id)}
          />
        )}
      />
      <Pressable className="absolute bottom-8 right-8 w-16 h-16 bg-primary rounded-full items-center justify-center shadow-lg shadow-black/30 elevation-5 active:scale-95 transition-transform">
        <Ionicons name="add" size={32} color="white" />
      </Pressable>
    </View>
  );
};

export default FridgeMealsScreen;
