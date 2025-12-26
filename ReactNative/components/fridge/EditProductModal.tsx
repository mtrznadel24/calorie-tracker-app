import {
  View,
  Text,
  Modal,
  Pressable,
  TextInput,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator, Alert,
} from 'react-native';
import React, {useEffect, useState} from 'react';
import { Ionicons } from '@expo/vector-icons';
import clsx from 'clsx';
import { FoodCategory, UpdateProductData} from "@/services/fridgeProductsService";
import { Product } from "@/services/fridgeProductsService"

const CATEGORIES_TO_SELECT = [
  "fruits", "vegetables", "meat and fish", "grains",
  "dairy", "snacks", "fats", "plant protein", "drinks"
];

interface AddProductModalProps {
  isVisible: boolean;
  onClose: () => void;
  onSubmit: (product: Product, data: UpdateProductData) => Promise<void>;
  onDelete: (product: Product) => Promise<void>;
  product: Product | null;
}

const EditProductModal = ({ isVisible, onClose, onSubmit, onDelete, product}: AddProductModalProps) => {
  const [isLoading, setIsLoading] = useState(false);

  const [name, setName] = useState("");
  const [category, setCategory] = useState<string | null>(null);
  const [calories, setCalories] = useState("");
  const [proteins, setProteins] = useState("");
  const [fats, setFats] = useState("");
  const [carbs, setCarbs] = useState("");
  const [isFavourite, setIsFavourite] = useState(false);

  useEffect(() => {
    if (product) {
      setName(product.product_name);
      setCategory(product.category);
      setCalories(product.calories_100g?.toString() || "");
      setProteins(product.proteins_100g?.toString() || "");
      setFats(product.fats_100g?.toString() || "");
      setCarbs(product.carbs_100g?.toString() || "");
      setIsFavourite(product.is_favourite);
    }
  }, [product, isVisible]);

  const handleSubmit = async () => {
    if (!product) return;

    setIsLoading(true);
    try {
      const payload: UpdateProductData = {
        product_name: name || undefined,
        category: category ? category as FoodCategory : undefined,
        calories_100g: calories ? parseFloat(calories) : undefined,
        proteins_100g: proteins ? parseFloat(proteins) : undefined,
        fats_100g: fats ? parseFloat(fats) : undefined,
        carbs_100g: carbs ? parseFloat(carbs) : undefined,
        is_favourite: isFavourite || undefined,
      };

      await onSubmit(product, payload);
      onClose();
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeletePress = () => {
    Alert.alert(
      "Delete Product",
      "Are you sure you want to remove this product from your fridge?",
      [
        {
          text: "Cancel",
          style: "cancel"
        },
        {
          text: "Delete",
          style: "destructive",
          onPress: handleDelete
        }
      ]
    );
  };

  const handleDelete = async () => {
    if (!product) return;

    setIsLoading(true);
    try {
      await onDelete(product);
      onClose();
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  if (!product) return null;

  return (
    <Modal
      animationType="slide"
      presentationStyle={Platform.OS === 'ios' ? 'pageSheet' : 'overFullScreen'}
      transparent={Platform.OS !== 'ios'}
      visible={isVisible}
      onRequestClose={onClose}
    >
      <View className="flex-1 justify-end bg-black/50">

        {Platform.OS !== 'ios' && (
             <Pressable className="absolute inset-0" onPress={onClose} />
        )}

        <View className={clsx(
              "h-[85%] w-full rounded-t-3xl overflow-hidden",
              Platform.OS === 'ios' ? "bg-white dark:bg-dark-900" : "bg-white dark:bg-dark-900"
          )}
        >

          <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : undefined}
            className="flex-1 relative"
          >
            {/* HEADER */}
            <View className="items-center pt-4 pb-2 bg-white dark:bg-dark-900 z-10">
              <View className="w-12 h-1.5 bg-gray-300 rounded-full mb-4" />

              <View className="flex-row justify-between items-center w-full px-6">
                <Text className="text-2xl font-bold text-dark-900 dark:text-text-light">
                  Edit Product
                </Text>

                <View className="flex-row gap-3">

                   <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-800 rounded-full">
                      <Ionicons name="close" size={24} color="gray" />
                   </Pressable>
                </View>
              </View>
            </View>

            <ScrollView
              className="flex-1 px-6 pt-2 bg-white dark:bg-dark-900"
              showsVerticalScrollIndicator={false}
              contentContainerStyle={{ paddingBottom: 200 }}
            >

              {/* PRODUCT NAME */}
              <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted mt-2">Product Name *</Text>
              <TextInput
                value={name}
                onChangeText={setName}
                placeholder="eg. apple"
                placeholderTextColor="#9CA3AF"
                className="p-4 rounded-xl border border-light-300 dark:border-dark-600 bg-light-50 dark:bg-dark-800 text-dark-900 dark:text-text-light mb-6"
              />

              {/* CATEGORY SELECTOR */}
              <Text className="mb-3 font-semibold text-dark-700 dark:text-text-muted">Category *</Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} className="mb-6 flex-row">
                 <View className="flex-row gap-2 pr-4">
                  {CATEGORIES_TO_SELECT.map((cat) => (
                      <Pressable
                      key={cat}
                      onPress={() => setCategory(cat)}
                      className={clsx(
                          "px-4 py-2 rounded-full border",
                          category === cat
                          ? "bg-primary border-primary"
                          : "bg-light-50 dark:bg-dark-800 border-light-300 dark:border-dark-600"
                      )}
                      >
                      <Text className={clsx("capitalize font-medium", category === cat ? "text-white" : "text-dark-700 dark:text-text-muted")}>
                          {cat}
                      </Text>
                      </Pressable>
                  ))}
                 </View>
              </ScrollView>

              {/* CALORIES */}
              <View className="flex-row gap-4 mb-4">
                  <View className="flex-1">
                      <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted">Calories per 100g (kcal)</Text>
                      <TextInput
                          value={calories}
                          onChangeText={setCalories}
                          keyboardType="numeric"
                          placeholder="eg. 150"
                          placeholderTextColor="#9CA3AF"
                          className="p-4 rounded-xl border border-light-300 dark:border-dark-600 bg-light-50 dark:bg-dark-800 text-dark-900 dark:text-text-light"
                      />
                  </View>
              </View>

              {/* MACROS GRID */}
              <Text className="mb-3 font-semibold text-dark-700 dark:text-text-muted">Macros per 100g</Text>
              <View className="flex-row gap-4">
                   {/* PROTEINS */}
                  <View className="flex-1">
                      <Text className="text-xs mb-1 text-dark-700 dark:text-text-muted">Proteins</Text>
                      <TextInput
                          value={proteins}
                          onChangeText={setProteins}
                          keyboardType="numeric"
                          placeholder="eg. 15"
                          className="p-3 rounded-xl border border-light-300 dark:border-dark-600 bg-light-50 dark:bg-dark-800 text-dark-900 dark:text-text-light"
                      />
                  </View>
                  {/* CARBS */}
                  <View className="flex-1">
                      <Text className="text-xs mb-1 text-dark-700 dark:text-text-muted">Carbs</Text>
                      <TextInput
                          value={carbs}
                          onChangeText={setCarbs}
                          keyboardType="numeric"
                          placeholder="eg. 35"
                          className="p-3 rounded-xl border border-light-300 dark:border-dark-600 bg-light-50 dark:bg-dark-800 text-dark-900 dark:text-text-light"
                      />
                  </View>
                  {/* FATS */}
                  <View className="flex-1">
                      <Text className="text-xs mb-1 text-dark-700 dark:text-text-muted">Fats</Text>
                      <TextInput
                          value={fats}
                          onChangeText={setFats}
                          keyboardType="numeric"
                          placeholder="eg. 10"
                          className="p-3 rounded-xl border border-light-300 dark:border-dark-600 bg-light-50 dark:bg-dark-800 text-dark-900 dark:text-text-light"
                      />
                  </View>
              </View>

            </ScrollView>

            {/* FOOTER BUTTONS */}
            <View className="p-6 border-t border-light-200 dark:border-dark-700 bg-white dark:bg-dark-900 absolute bottom-0 w-full pb-10 gap-3">

              <Pressable
                  onPress={handleSubmit}
                  disabled={isLoading}
                  className={clsx(
                      "p-4 rounded-xl items-center shadow-sm",
                      (!name || !category) ? "bg-gray-300 dark:bg-dark-700" : "bg-primary"
                  )}
              >
                  {isLoading ? <ActivityIndicator color="white" /> : <Text className="text-white font-bold text-lg">Save Changes</Text>}
              </Pressable>

              <Pressable
                  onPress={handleDeletePress}
                  disabled={isLoading}
                  className="p-4 rounded-xl items-center border border-red-500 bg-transparent active:bg-red-50 dark:active:bg-red-900/20"
              >
                  <Text className="text-red-500 font-bold text-lg">Delete Product</Text>
              </Pressable>

            </View>

          </KeyboardAvoidingView>
        </View>
      </View>
    </Modal>
  );
};

export default EditProductModal;