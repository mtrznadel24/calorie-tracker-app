import React, { useState } from "react";
import {
  Modal,
  Platform,
  Pressable,
  View,
  Text,
  TextInput,
  KeyboardAvoidingView,
  ScrollView,
  ActivityIndicator
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import clsx from "clsx";
import FridgeProductList from "@/components/fridge/FridgeProductList";
import FridgeMealList from "@/components/fridge/FridgeMealList";
import { Product } from "@/services/fridgeProductsService";
import { Meal } from "@/services/fridgeMealsService";
import Toast from "react-native-toast-message";
import {QuickAddLogData, SimpleProductData} from "@/services/mealService";


interface AddMealLogModalProps {
  isVisible: boolean;
  onClose: () => void;
  onQuickSubmit: (data: SimpleProductData) => void;
  onProductSubmit: (product: Product) => Promise<void>;
  onMealSubmit: (meal: Meal) => Promise<void>;
  sectionTitle: string | null;
}

type TabType = 'products' | 'meals' | 'quick';

const AddMealLogModal = ({ isVisible, onClose, onQuickSubmit, onProductSubmit, onMealSubmit, sectionTitle }: AddMealLogModalProps) => {
  const [activeTab, setActiveTab] = useState<TabType>('products');

  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [weight, setWeight] = useState("");

  const [quickName, setQuickName] = useState("");
  const [quickCals, setQuickCals] = useState("");
  const [quickProt, setQuickProt] = useState("");
  const [quickFat, setQuickFat] = useState("");
  const [quickCarb, setQuickCarb] = useState("");
  const [quickWeight, setQuickWeight] = useState("100");

  const [isLoading, setIsLoading] = useState(false);

  const handleProductSelect = (product: Product) => {
    setSelectedProduct(product);
    setWeight("");
  };

  const submitProduct = async () => {
    if (!selectedProduct || !weight) return;
    setIsLoading(true);
    try {

      await onProductSubmit(selectedProduct);
      resetAndClose();
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleMealSelect = async (meal: Meal) => {
    setIsLoading(true);
    try {
      await onMealSubmit(meal);
      resetAndClose();
      Toast.show({ type: 'success', text1: 'Meal added successfully' });
    } catch (e) {
        console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAdd = async () => {
    if (!quickName || !quickCals || !sectionTitle) return;
    setIsLoading(true);
    try {
        const logData: SimpleProductData = {
            name: quickName,
            weight: parseFloat(quickWeight) || 100,
            calories_100g: parseFloat(quickCals),
            proteins_100g: parseFloat(quickProt) || 0,
            fats_100g: parseFloat(quickFat) || 0,
            carbs_100g: parseFloat(quickCarb) || 0,
        };
        await onQuickSubmit(logData);
        resetAndClose();
    } catch (e) {
        console.error(e);
    } finally {
        setIsLoading(false);
    }
  };

  const resetAndClose = () => {
    setSelectedProduct(null);
    setWeight("");
    setQuickWeight("");
    setQuickName("");
    setQuickCals("");
    setQuickProt("");
    setQuickFat("");
    setQuickCarb("");
    onClose();
  };

  if (selectedProduct) {
    return (
      <Modal animationType="slide" visible={isVisible} presentationStyle="pageSheet" onRequestClose={() => setSelectedProduct(null)}>
         <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} className="flex-1 bg-white dark:bg-dark-900 justify-center px-6">
            <Pressable onPress={() => setSelectedProduct(null)} className="absolute top-6 left-4 z-10 p-2 bg-light-100 dark:bg-dark-800 rounded-full">
                <Ionicons name="arrow-back" size={24} color="gray" />
            </Pressable>

            <View className="items-center w-full">
                <Text className="text-2xl font-bold mb-2 dark:text-white text-center">How much {selectedProduct.product_name}?</Text>
                <Text className="text-gray-500 mb-8">{selectedProduct.calories_100g} kcal / 100g</Text>

                <View className="flex-row items-end justify-center gap-2 mb-10">
                    <TextInput
                        value={weight} onChangeText={setWeight} keyboardType="numeric" autoFocus
                        placeholder="0" className="text-6xl font-bold text-primary border-b-2 border-primary min-w-[100px] text-center"
                    />
                    <Text className="text-2xl text-gray-400 pb-4">g</Text>
                </View>

                <Pressable onPress={submitProduct} disabled={!weight || isLoading} className="w-full bg-primary p-4 rounded-xl items-center">
                    {isLoading ? <ActivityIndicator color="white"/> : <Text className="text-white font-bold text-lg">Add to {sectionTitle}</Text>}
                </Pressable>
            </View>
         </KeyboardAvoidingView>
      </Modal>
    );
  }

  return (
    <Modal animationType="slide" visible={isVisible} presentationStyle="pageSheet" onRequestClose={onClose}>
      <View className="flex-1 bg-white dark:bg-dark-900">
        <View className="flex-row justify-between items-center p-4 border-b border-light-200 dark:border-dark-800">
            <Text className="text-xl font-bold dark:text-white">Add to {sectionTitle}</Text>
            <Pressable onPress={onClose} className="p-2 bg-light-100 dark:bg-dark-800 rounded-full">
                <Ionicons name="close" size={24} color="gray" />
            </Pressable>
        </View>

        <View className="flex-row px-4 pt-2 pb-2 gap-4">
            {['products', 'meals', 'quick'].map((tab) => (
                <Pressable
                    key={tab}
                    onPress={() => setActiveTab(tab as TabType)}
                    className={clsx(
                        "flex-1 py-3 items-center border-b-2",
                        activeTab === tab ? "border-primary" : "border-transparent"
                    )}
                >
                    <Text className={clsx(
                        "font-bold capitalize",
                        activeTab === tab ? "text-primary" : "text-gray-400"
                    )}>{tab === 'quick' ? 'Quick Add' : tab}</Text>
                </Pressable>
            ))}
        </View>

        <View className="flex-1 bg-light-50 dark:bg-dark-900">
            {activeTab === 'products' && (
                <FridgeProductList
                    onProductPress={handleProductSelect}
                    onAddButtonPress={() => {}}
                />
            )}

            {activeTab === 'meals' && (
                <FridgeMealList onMealPress={handleMealSelect} />
            )}

            {activeTab === 'quick' && (
              <ScrollView
                  className="flex-1 px-5 pt-6"
                  keyboardShouldPersistTaps="handled"
                  contentContainerStyle={{ paddingBottom: 40 }}
              >
                  <View className="mb-6">
                      <Text className="text-sm font-bold text-gray-500 uppercase tracking-widest mb-4">
                          Basic Info
                      </Text>

                      <View className="mb-4">
                          <Text className="text-base font-semibold text-dark-900 dark:text-white mb-2 ml-1">
                              Product Name
                          </Text>
                          <TextInput
                              value={quickName}
                              onChangeText={setQuickName}
                              placeholder="e.g. Homemade Cookie"
                              placeholderTextColor="#9CA3AF"
                              className="w-full bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-4 py-3.5 text-base text-dark-900 dark:text-white"
                          />
                      </View>

                      <View>
                          <Text className="text-base font-semibold text-dark-900 dark:text-white mb-2 ml-1">
                              Consumed Weight <Text className="text-gray-400 font-normal">(g)</Text>
                          </Text>
                          <TextInput
                              value={quickWeight}
                              onChangeText={setQuickWeight}
                              keyboardType="numeric"
                              placeholder="100"
                              placeholderTextColor="#9CA3AF"
                              className="w-full bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-4 py-3.5 text-base text-dark-900 dark:text-white"
                          />
                      </View>
                  </View>

                  <View className="mb-6">
                      <View className="flex-row items-center mb-4">
                          <Text className="text-sm font-bold text-gray-500 uppercase tracking-widest flex-1">
                              Nutritional Values
                          </Text>
                          <View className="bg-primary/10 px-2 py-1 rounded-md">
                              <Text className="text-primary text-xs font-bold">PER 100g</Text>
                          </View>
                      </View>

                      <View className="mb-4">
                          <Text className="text-base font-semibold text-dark-900 dark:text-white mb-2 ml-1">
                              Energy <Text className="text-gray-400 font-normal">(kcal)</Text>
                          </Text>
                          <TextInput
                              value={quickCals}
                              onChangeText={setQuickCals}
                              keyboardType="numeric"
                              placeholder="0"
                              placeholderTextColor="#9CA3AF"
                              className="w-full bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-4 py-3.5 text-base text-dark-900 dark:text-white"
                          />
                      </View>

                      <View className="flex-row gap-3">
                          <View className="flex-1">
                              <Text className="text-sm font-semibold text-dark-900 dark:text-gray-300 mb-2 ml-1">
                                  Protein
                              </Text>
                              <TextInput
                                  value={quickProt}
                                  onChangeText={setQuickProt}
                                  keyboardType="numeric"
                                  placeholder="0"
                                  placeholderTextColor="#9CA3AF"
                                  className="w-full bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-3 py-3 text-center text-base text-dark-900 dark:text-white"
                              />
                          </View>
                          <View className="flex-1">
                              <Text className="text-sm font-semibold text-dark-900 dark:text-gray-300 mb-2 ml-1">
                                  Fat
                              </Text>
                              <TextInput
                                  value={quickFat}
                                  onChangeText={setQuickFat}
                                  keyboardType="numeric"
                                  placeholder="0"
                                  placeholderTextColor="#9CA3AF"
                                  className="w-full bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-3 py-3 text-center text-base text-dark-900 dark:text-white"
                              />
                          </View>
                          <View className="flex-1">
                              <Text className="text-sm font-semibold text-dark-900 dark:text-gray-300 mb-2 ml-1">
                                  Carbs
                              </Text>
                              <TextInput
                                  value={quickCarb}
                                  onChangeText={setQuickCarb}
                                  keyboardType="numeric"
                                  placeholder="0"
                                  placeholderTextColor="#9CA3AF"
                                  className="w-full bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-3 py-3 text-center text-base text-dark-900 dark:text-white"
                              />
                          </View>
                      </View>
                  </View>

                  <Pressable
                    onPress={handleQuickAdd}
                    disabled={!quickName || !quickWeight || !quickCals}
                    className={clsx(
                        "w-full py-4 rounded-2xl items-center shadow-lg mt-2",
                        (!quickName || !quickWeight || !quickCals)
                            ? "bg-gray-300 dark:bg-dark-600 shadow-none"
                            : "bg-primary shadow-primary/30 active:opacity-90"
                    )}
                  >
                    <Text className={clsx(
                        "font-bold text-lg tracking-wide",
                        (!quickName || !quickWeight || !quickCals) ? "text-gray-500" : "text-white"
                    )}>
                        Add Product
                    </Text>
                  </Pressable>
              </ScrollView>
            )}
        </View>
      </View>
    </Modal>
  );
};

export default AddMealLogModal;