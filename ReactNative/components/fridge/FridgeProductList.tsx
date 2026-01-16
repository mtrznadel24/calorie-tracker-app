import fridgeProductsService, { AddProductData, Product } from "@/services/fridgeProductsService";
import React, { useEffect, useMemo, useState } from "react";
import Toast from "react-native-toast-message";
import { ActivityIndicator, FlatList, Pressable, Text, View } from "react-native";
import SearchBar from "@/components/SearchBar";
import { Ionicons } from "@expo/vector-icons";
import AddProductModal from "@/components/fridge/AddProductModal";

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

interface FridgeProductListProps {
  onProductPress: (product: Product) => void;
  onAddButtonPress: (product: Product) => void;
  onToggleFavourite?: (product: Product) => void;
}

const FridgeProductList = ({
  onProductPress,
  onAddButtonPress,
  onToggleFavourite,
}: FridgeProductListProps) => {
  const [searchText, setSearchText] = useState("");
  const [showFavourites, setShowFavourites] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [products, setProducts] = useState<Product[]>([]);
  const [isFetching, setIsFetching] = useState(true);
  const [isAddProductModalOpen, setIsAddProductModalOpen] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsFetching(true);
        const data = await fridgeProductsService.getProducts();
        setProducts(data);
      } catch (error) {
        console.log(error);
        Toast.show({
          type: "error",
          text1: "Fetching data fail",
          text2: "Something went wrong ❌",
        });
      } finally {
        setIsFetching(false);
      }
    };
    fetchData();
  }, []);

  const filteredProducts = useMemo(() => {
    return products.filter((item) => {
      const matchesSearch = item.product_name
        .toLowerCase()
        .includes(searchText.toLowerCase());
      const matchesCategory =
        selectedCategory === "All" || item.category === selectedCategory;
      const matchesFavourite = !showFavourites || item.is_favourite;
      return matchesSearch && matchesCategory && matchesFavourite;
    });
  }, [products, searchText, selectedCategory, showFavourites]);

  const handleAddProduct = async (newProductData: AddProductData) => {
    try {
      const newProduct = await fridgeProductsService.addProduct(newProductData);
      setProducts((prev) => [...prev, newProduct]);
      setIsAddProductModalOpen(false);

      Toast.show({
        type: "success",
        text1: "Product added!",
      });

      onAddButtonPress(newProduct);
    } catch (error) {
      console.log(error);
      Toast.show({ type: "error", text1: "Failed to add product" });
    }
  };

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

      {isFetching ? (
        <View className="flex-1 justify-center items-center mt-10">
          <ActivityIndicator size="large" color="#3b82f6" />
        </View>
      ) : (
        <FlatList
          data={filteredProducts}
          keyExtractor={(item) => item.id.toString()}
          className="mt-2"
          contentContainerStyle={{ paddingBottom: 100, paddingTop: 10, paddingHorizontal: 16 }}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <View className="items-center justify-center mt-10">
              <Ionicons
                name="fast-food-outline"
                size={48}
                color="gray"
                opacity={0.5}
              />
              <Text className="text-gray-400 mt-2">No products found</Text>
            </View>
          }
          renderItem={({ item }) => (
            <Pressable
              onPress={() => onProductPress(item)}
              className="bg-white dark:bg-dark-700 p-3.5 rounded-2xl mb-3 shadow-sm border border-light-200 dark:border-dark-700 active:bg-gray-50 dark:active:bg-dark-700 flex-row justify-between items-center"
            >
              {/* LEWA STRONA: Nazwa, Kategoria, Ikona */}
              <View className="flex-1 pr-4 justify-center">
                <Text
                  className="text-base font-bold text-dark-900 dark:text-gray-100 mb-1.5"
                  numberOfLines={1}
                  ellipsizeMode="tail"
                >
                  {item.product_name}
                </Text>

                <View className="flex-row items-center flex-wrap">
                  {/* Ikona kategorii (uniwersalna nutrition lub leaf) */}
                  <Ionicons
                    name="nutrition-outline"
                    size={12}
                    color="#9CA3AF"
                    style={{ marginRight: 4 }}
                  />
                  <Text className="text-xs text-gray-400 font-medium capitalize">
                    {item.category} • 100g
                  </Text>

                  {/* Serduszko informacyjne w linii tekstu */}
                  {item.is_favourite && (
                    <>
                      <Text className="text-xs text-gray-400 font-medium mx-1">
                        •
                      </Text>
                      <Ionicons name="heart" size={12} color="#EF4444" />
                    </>
                  )}
                </View>
              </View>

              {/* PRAWA STRONA: Kalorie i Makro na 100g */}
              <View className="items-end justify-center">
                <View className="flex-row items-baseline mb-1">
                  <Text className="text-lg font-extrabold text-primary dark:text-blue-400">
                    {item.calories_100g.toFixed(0)}
                  </Text>
                  <Text className="text-xs text-gray-400 ml-0.5 font-medium">
                    kcal
                  </Text>
                </View>

                <View className="flex-row items-center gap-2">
                  {/* Białko */}
                  <View className="flex-row items-center bg-blue-50 dark:bg-blue-900/20 px-1.5 py-0.5 rounded-md">
                    <Text className="text-[10px] font-black text-blue-600 dark:text-blue-400 mr-1">
                      P
                    </Text>
                    <Text className="text-[10px] font-bold text-gray-600 dark:text-gray-300">
                      {item.proteins_100g.toFixed(0)}
                    </Text>
                  </View>

                  {/* Tłuszcze */}
                  <View className="flex-row items-center bg-yellow-50 dark:bg-yellow-900/20 px-1.5 py-0.5 rounded-md">
                    <Text className="text-[10px] font-black text-yellow-600 dark:text-yellow-400 mr-1">
                      F
                    </Text>
                    <Text className="text-[10px] font-bold text-gray-600 dark:text-gray-300">
                      {item.fats_100g.toFixed(0)}
                    </Text>
                  </View>

                  {/* Węglowodany */}
                  <View className="flex-row items-center bg-orange-50 dark:bg-orange-900/20 px-1.5 py-0.5 rounded-md">
                    <Text className="text-[10px] font-black text-orange-600 dark:text-orange-400 mr-1">
                      C
                    </Text>
                    <Text className="text-[10px] font-bold text-gray-600 dark:text-gray-300">
                      {item.carbs_100g.toFixed(0)}
                    </Text>
                  </View>
                </View>
              </View>
            </Pressable>
          )}
        />
      )}

      {/* Przycisk dodawania */}
      <Pressable
        onPress={() => setIsAddProductModalOpen(true)}
        className="absolute bottom-8 right-8 w-16 h-16 bg-primary rounded-full items-center justify-center shadow-lg shadow-black/30 elevation-5 active:scale-95 transition-transform"
      >
        <Ionicons name="add" size={32} color="white" />
      </Pressable>

      <AddProductModal
        isVisible={isAddProductModalOpen}
        onClose={() => setIsAddProductModalOpen(false)}
        onSubmit={handleAddProduct}
      />
    </View>
  );
};

export default FridgeProductList;