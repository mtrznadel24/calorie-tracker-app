import fridgeProductsService, {AddProductData, Product} from "@/services/fridgeProductsService";
import fridgeMealsService, {
  AddIngredientData,
  AddMealData,
  Ingredient,
  IngredientDisplayItem
} from "@/services/fridgeMealsService";
import React, {useEffect, useState} from "react";
import {
  ActivityIndicator, FlatList,
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  Text,
  TextInput,
  View
} from "react-native";
import clsx from "clsx";
import {Ionicons} from "@expo/vector-icons";
import AddIngredientModal from "@/components/fridge/AddIngredientModal";


interface AddMealModalProps {
  isVisible: boolean;
  onClose: () => void;
  onSubmit: (data: AddMealData) => Promise<void>;
}


const AddMealModal = ({isVisible, onClose, onSubmit}: AddMealModalProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [name, setName] = useState("");
  const [isFavourite, setIsFavourite] = useState(false);
  const [ingredients, setIngredients] = useState<IngredientDisplayItem[]>([]);
  const [isAddIngredientModalOpen, setIsAddIngredientModalOpen] = useState(false);

  const handleSubmit = async () => {
    if (!name) return;
    setIsLoading(true);
    try {
      const IngredientsPayload: Ingredient[] = ingredients.map(item => ({
        weight: item.weight,
        fridge_product_id: item.fridge_product_id
      }));

      const payload: AddMealData = {
        name: name,
        is_favourite: isFavourite,
        ingredients: IngredientsPayload
      }
      await onSubmit(payload);
      resetForm();
      setIngredients([])
      onClose();
    } catch (error) {
      console.error(error);
      resetForm();
      setIngredients([])
    } finally {
      setIsLoading(false);
    }
  }

  const resetForm = () => {
    setName("");
    setIsFavourite(false);
  };

  const handleRemoveIngredient = (id?: string) => {
    if (id === null) return;
    setIngredients(prev => prev.filter(item => item.tempId !== id));
  }

  const handleAddIngredient = async (product: Product, data: AddIngredientData) => {
    const calculatedCalories = (product.calories_100g * data.weight) / 100;

    const newItem: IngredientDisplayItem = {
      tempId: Math.random().toString(),
      fridge_product_id: data.fridge_product_id,
      weight: data.weight,
      product_name: product.product_name,
      calories: calculatedCalories
    };

    setIngredients(prevIngredients => [...prevIngredients, newItem])
  }

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
                  Add Meal
                </Text>

                <View className="flex-row gap-3">
                   <Pressable
                      onPress={() => setIsFavourite(!isFavourite)}
                      className={clsx(
                          "p-2 rounded-full border",
                          isFavourite ? "bg-red-50 border-red-100 dark:bg-red-900/20 dark:border-red-900" : "bg-light-200 border-light-200 dark:bg-dark-800 dark:border-dark-700"
                      )}
                   >
                      <Ionicons
                          name={isFavourite ? "heart" : "heart-outline"}
                          size={24}
                          color={isFavourite ? "#EF4444" : "gray"}
                      />
                   </Pressable>

                   <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-800 rounded-full">
                      <Ionicons name="close" size={24} color="gray" />
                   </Pressable>
                </View>
              </View>
            </View>

            <ScrollView
              className="flex-1 px-6 pt-2 bg-white dark:bg-dark-900"
              showsVerticalScrollIndicator={false}
              contentContainerStyle={{ paddingBottom: 120 }}
            >

              {/* PRODUCT NAME */}
              <Text className="mb-2 font-semibold text-dark-700 dark:text-text-muted mt-2">Meal Name *</Text>
              <TextInput
                value={name}
                onChangeText={setName}
                placeholder="e.g. Chicken and rice"
                placeholderTextColor="#9CA3AF"
                className="p-4 rounded-xl border border-light-300 dark:border-dark-600 bg-light-50 dark:bg-dark-800 text-dark-900 dark:text-text-light mb-6"
              />
              <Pressable
                onPress={() => setIsAddIngredientModalOpen(true)}
                disabled={isLoading}
                className="p-4 rounded-xl items-center shadow-sm bg-primary"
              >
                <Text className="text-white font-bold text-lg">Add Ingredient</Text>
              </Pressable>

              <View className="gap-3 mt-4">
                {ingredients.length === 0 ? (
                    <View className="items-center justify-center py-6 border border-dashed border-gray-300 dark:border-dark-700 rounded-xl">
                        <Text className="text-gray-400">No ingredients added yet</Text>
                    </View>
                ) : (
                    ingredients.map((item) => (
                        <View
                            key={item.tempId}
                            className="flex-row items-center justify-between p-3 bg-light-50 dark:bg-dark-800 rounded-xl border border-light-200 dark:border-dark-700"
                        >
                            <View className="flex-1">
                                <Text className="font-semibold text-dark-900 dark:text-white text-lg">
                                    {item.product_name}
                                </Text>
                                <Text className="text-sm text-gray-500">
                                    {item.weight}g • {item.calories.toFixed(0)} kcal
                                </Text>
                            </View>

                            <Pressable
                                onPress={() => handleRemoveIngredient(item.tempId)}
                                className="p-2"
                            >
                                <Ionicons name="trash-outline" size={20} color="#EF4444" />
                            </Pressable>
                        </View>
                    ))
                )}
              </View>

            </ScrollView>

            {/* FOOTER BUTTON */}
            <View className="p-6 border-t border-light-200 dark:border-dark-700 bg-white dark:bg-dark-900 absolute bottom-0 w-full pb-10">
              <Pressable
                  onPress={handleSubmit}
                  disabled={isLoading || !name}
                  className={clsx(
                      "p-4 rounded-xl items-center shadow-sm",
                      (!name) ? "bg-gray-300 dark:bg-dark-700" : "bg-primary"
                  )}
              >
                  {isLoading ? <ActivityIndicator color="white" /> : <Text className="text-white font-bold text-lg">Add to Fridge</Text>}
              </Pressable>
            </View>
            <AddIngredientModal
              isVisible={isAddIngredientModalOpen}
              onClose={() => setIsAddIngredientModalOpen(false)}
              onSubmit={handleAddIngredient}
            />

          </KeyboardAvoidingView>
        </View>
      </View>
    </Modal>
  );
};

export default AddMealModal;