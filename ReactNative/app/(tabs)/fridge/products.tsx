import { View, Text, Pressable, FlatList } from "react-native";
import React, { useState } from "react";
import SearchBar from "@/components/SearchBar";
import { Ionicons } from "@expo/vector-icons";
import ProductCard from "@/components/ProductCard";

const CATEGORIES = [
  "All",
  "fruits",
  "vegetables",
  "meat and fish",
  "grains",
  "dairy",
  "snacks",
  "fats",
  "plant protein",
  "drinks",
];

const FridgeProductsScreen = () => {
  const [searchText, setSearchText] = useState("");
  const [showFavourites, setShowFavourites] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [products, setProducts] = useState([
    {
      id: 1,
      name: "Apple",
      category: "fruits",
      isFavourite: true,
      calories_100g: 52,
      proteins_100g: 0.3,
      fats_100g: 0.2,
      carbs_100g: 14,
    },
    {
      id: 2,
      name: "Chicken Breast",
      category: "meat and fish",
      isFavourite: false,
      calories_100g: 165,
      proteins_100g: 31,
      fats_100g: 3.6,
      carbs_100g: 0,
    },
    {
      id: 3,
      name: "Greek Yogurt",
      category: "dairy",
      isFavourite: false,
      calories_100g: 59,
      proteins_100g: 10,
      fats_100g: 0.4,
      carbs_100g: 3.6,
    },
    {
      id: 4,
      name: "Banana",
      category: "fruits",
      isFavourite: false,
      calories_100g: 89,
      proteins_100g: 1.1,
      fats_100g: 0.3,
      carbs_100g: 23,
    },
    {
      id: 5,
      name: "Broccoli",
      category: "vegetables",
      isFavourite: true,
      calories_100g: 34,
      proteins_100g: 2.8,
      fats_100g: 0.4,
      carbs_100g: 7,
    },
  ]);

  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-800 relative">
      <View className="flex-row items-center gap-3 px-3 py-3 bg-light-100 dark:bg-dark-800 z-10">
        <View className="flex-1 h-12">
          <SearchBar
            value={searchText}
            onChangeText={setSearchText}
            placeholder="Search products"
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

      <View>
        <FlatList
          horizontal
          data={CATEGORIES}
          keyExtractor={(item) => item}
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={{ paddingHorizontal: 12, gap: 8 }}
          renderItem={({ item }) => {
            const isSelected = selectedCategory === item;
            return (
              <Pressable
                onPress={() => setSelectedCategory(item)}
                className={`px-4 py-2 rounded-full border ${
                  isSelected
                    ? "bg-primary border-primary"
                    : "bg-white dark:bg-dark-700 border-light-300 dark:border-dark-600"
                }`}
              >
                <Text
                  className={`font-medium capitalize ${
                    isSelected
                      ? "text-white"
                      : "text-text-dark dark:text-text-light"
                  }`}
                >
                  {item}
                </Text>
              </Pressable>
            );
          }}
        />
      </View>

      <FlatList
        data={products}
        keyExtractor={(item) => item.id.toString()}
        className="mt-2"
        contentContainerStyle={{ paddingBottom: 100, paddingTop: 10 }}
        showsVerticalScrollIndicator={false}
        renderItem={({ item }) => (
          <ProductCard
            id={item.id}
            name={item.name}
            category={item.category}
            calories={item.calories_100g}
            proteins={item.proteins_100g}
            fats={item.fats_100g}
            carbs={item.carbs_100g}
            isFavourite={item.isFavourite}
            onToggleFavourite={() =>
              console.log("Clicked heart icon ID:", item.id)
            }
            onPress={() => console.log("Open product details ID:", item.id)}
          />
        )}
      />

      <Pressable className="absolute bottom-8 right-8 w-16 h-16 bg-primary rounded-full items-center justify-center shadow-lg shadow-black/30 elevation-5 active:scale-95 transition-transform">
        <Ionicons name="add" size={32} color="white" />
      </Pressable>
    </View>
  );
};

export default FridgeProductsScreen;
