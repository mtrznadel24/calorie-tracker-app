import React, { useState } from "react";
import {
  Modal,
  View,
  Text,
  TextInput,
  Pressable,
  Platform,
  KeyboardAvoidingView
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { AddIngredientData } from "@/services/fridgeMealsService";
import {Product} from "@/services/fridgeProductsService";
import FridgeProductList from "@/components/fridge/FridgeProductList";
import clsx from "clsx";

interface AddIngredientModalProps {
  isVisible: boolean;
  onClose: () => void;
  onSubmit: (product: Product, data: AddIngredientData) => Promise<void>;
}

const AddIngredientModal = ({ isVisible, onClose, onSubmit }: AddIngredientModalProps) => {
  const [selectedIngredient, setSelectedIngredient] = useState<Product | null>(null);
  const [weight, setWeight] = useState("");

  const handleSelectIngredient = (product: Product) => {
    setSelectedIngredient(product);
    setWeight("");
  };

  const handleBackToList = () => {
    setSelectedIngredient(null);
  };

  const handleSubmit = async () => {
    if (!selectedIngredient || !weight) return;

    const data: AddIngredientData = {
      fridge_product_id: selectedIngredient.id,
      weight: parseFloat(weight)
    };

    await onSubmit(selectedIngredient, data);

    setSelectedIngredient(null);
    setWeight("");
    onClose();
  };

  const handleClose = () => {
    setSelectedIngredient(null);
    setWeight("");
    onClose();
  }

  const handleAddButtonPress = async (ingredient: Product) => {
    setSelectedIngredient(ingredient);
  }

  return (
    <Modal
      animationType="slide"
      presentationStyle={Platform.OS === 'ios' ? 'pageSheet' : 'overFullScreen'}
      visible={isVisible}
      onRequestClose={handleClose}
      transparent={Platform.OS !== 'ios'}
    >
       {Platform.OS !== 'ios' && (
          <View className="absolute inset-0 bg-black/50" />
       )}

      {!selectedIngredient && (
        <View className={clsx(
            "flex-1 bg-white dark:bg-dark-900 overflow-hidden",
            Platform.OS !== 'ios' && "mt-10 rounded-t-3xl"
        )}>
           <View className="flex-row justify-between items-center px-4 py-4 border-b border-light-200 dark:border-dark-700">
              <Text className="text-xl font-bold dark:text-white">Select Ingredient</Text>
              <Pressable onPress={handleClose} className="p-2 bg-light-200 dark:bg-dark-800 rounded-full">
                <Ionicons name="close" size={24} color="gray" />
              </Pressable>
           </View>

           <FridgeProductList
              onProductPress={handleSelectIngredient}
              onAddButtonPress={handleAddButtonPress}
           />
        </View>
      )}

      {selectedIngredient && (
        <KeyboardAvoidingView
            behavior={Platform.OS === "ios" ? "padding" : undefined}
            className={clsx(
                "flex-1 bg-white dark:bg-dark-900 justify-center px-6 relative",
                 Platform.OS !== 'ios' && "mt-10 rounded-t-3xl"
            )}
        >
          <Pressable onPress={handleBackToList} className="absolute top-6 left-4 z-10 p-2 bg-light-100 dark:bg-dark-800 rounded-full">
             <Ionicons name="arrow-back" size={24} color="gray" />
          </Pressable>

          <Pressable onPress={handleClose} className="absolute top-6 right-4 z-10 p-2 bg-light-100 dark:bg-dark-800 rounded-full">
             <Ionicons name="close" size={24} color="gray" />
          </Pressable>

          <View className="items-center w-full">
            <Text className="text-2xl font-bold mb-2 dark:text-white text-center">
              Enter weight for {selectedIngredient.product_name}
            </Text>

            <Text className="text-sm text-gray-500 mb-8">
               {selectedIngredient.calories_100g} kcal per 100g
            </Text>

            <View className="flex-row items-end justify-center gap-2 mb-10 w-full">
                <TextInput
                    value={weight}
                    onChangeText={setWeight}
                    keyboardType="numeric"
                    autoFocus={true}
                    placeholder="0"
                    placeholderTextColor="#9CA3AF"
                    className="text-6xl font-bold text-primary border-b-2 border-primary min-w-[120px] text-center pb-2 bg-transparent"
                />
                <Text className="text-2xl text-gray-400 pb-4 font-medium">g</Text>
            </View>

            <Pressable
                onPress={handleSubmit}
                disabled={!weight}
                className={clsx(
                    "w-full p-4 rounded-xl items-center shadow-sm active:scale-95 transition-transform",
                    weight ? "bg-primary" : "bg-gray-300 dark:bg-dark-700"
                )}
            >
                <Text className="text-white font-bold text-lg">Add Ingredient</Text>
            </Pressable>
          </View>
        </KeyboardAvoidingView>
      )}
    </Modal>
  );
}

export default AddIngredientModal;