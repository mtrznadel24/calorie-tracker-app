import fridgeMealsService, {
  AddIngredientData,
  AddMealData,
  Ingredient,
  IngredientDisplayItem,
  Meal, UpdateMealData
} from "@/services/fridgeMealsService";
import React, {useEffect, useState} from "react";
import {Product} from "@/services/fridgeProductsService";
import {
  ActivityIndicator, Alert,
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
import FridgeMealsService from "@/services/fridgeMealsService";
import Toast from "react-native-toast-message";

interface EditMealModalProps {
  isVisible: boolean;
  onClose: (shouldRefresh?: boolean) => void;
  onSubmit: (data: UpdateMealData) => Promise<void>;
  onDelete: (meal: Meal) => void;
  meal: Meal | null;
}

const EditMealModal = ({isVisible, onClose, onSubmit, onDelete, meal}: EditMealModalProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [name, setName] = useState("");
  const [ingredients, setIngredients] = useState<IngredientDisplayItem[]>([]);
  const [isAddIngredientModalOpen, setIsAddIngredientModalOpen] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    const fetchProducts = async () => {
      setIsLoading(true);
      try {
        if (!meal) return;
        setName(meal.name);
        const products = await fridgeMealsService.getMealIngredients(meal.id);
        console.log("works yet products", products);
        setIngredients(products);
        setHasChanges(false)
      } catch (error) {

      } finally {
        setIsLoading(false);
      }
    }
    fetchProducts();
  }, [meal, isVisible]);

  const handleSubmit = async () => {
    if (!name) return;
    setIsLoading(true);
    try {

      const payload: UpdateMealData = {
        name: name,
      }
      await onSubmit(payload);
      resetForm();
      setIngredients([])
      onClose(true);
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
  };

  const handleClose = () => {
    onClose(hasChanges);
  };

  const handleRemoveIngredient = async (ingredient: IngredientDisplayItem) => {
    if (meal === null) {
      return;
    }
    if (!ingredient.id) return;
    try {
      await fridgeMealsService.deleteMealIngredient(meal.id, ingredient.id)
      setIngredients(prev => prev.filter(item => item.id !== ingredient.id));
      setHasChanges(true);
      Toast.show({
        type: 'success',
        text1: 'Ingredient deleted successfully',
      });
    } catch (error) {
      console.log(error);
      Toast.show({
        type: 'error',
        text1: 'removing ingredient failed',
        });
    }
  }

  const handleAddIngredient = async (product: Product, data: AddIngredientData) => {
    if (meal === null) { return; }
    try {
      const ingredient = await FridgeMealsService.addFridgeMealIngredient(meal.id, data)

      setIngredients(prevIngredients => [...prevIngredients, ingredient])
      setHasChanges(true);
      Toast.show({
        type: 'success',
        text1: 'Ingredient added successfully',
      });
    } catch (error) {
      console.error(error);
      Toast.show({
        type: 'error',
        text1: 'adding ingredient failed',
      });
    }
  }

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
    if (!meal) return;

    setIsLoading(true);
    try {
      await onDelete(meal);
      onClose();
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };



  return (
    <Modal
      animationType="slide"
      presentationStyle={Platform.OS === 'ios' ? 'pageSheet' : 'overFullScreen'}
      transparent={Platform.OS !== 'ios'}
      visible={isVisible}
      onRequestClose={handleClose}
    >
      <View className="flex-1 justify-end bg-black/50">

        {Platform.OS !== 'ios' && (
             <Pressable className="absolute inset-0" onPress={handleClose} />
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
                  Edit Meal
                </Text>
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
                            key={item.id}
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
                                onPress={() => handleRemoveIngredient(item)}
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
            <View className="p-6 border-t border-light-200 dark:border-dark-700 bg-white dark:bg-dark-900 absolute bottom-0 w-full pb-10 gap-3">
              <Pressable
                  onPress={handleSubmit}
                  disabled={isLoading || !name}
                  className={clsx(
                      "p-4 rounded-xl items-center shadow-sm",
                      (!name) ? "bg-gray-300 dark:bg-dark-700" : "bg-primary"
                  )}
              >
                  {isLoading ? <ActivityIndicator color="white" /> : <Text className="text-white font-bold text-lg">Update Name</Text>}
              </Pressable>

              <Pressable
                  onPress={handleDeletePress}
                  disabled={isLoading}
                  className="p-4 rounded-xl items-center border border-red-500 bg-transparent active:bg-red-50 dark:active:bg-red-900/20"
              >
                  <Text className="text-red-500 font-bold text-lg">Delete Product</Text>
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
}

export default EditMealModal;