import {
  View,
  Text,
  Modal,
  TextInput,
  Pressable,
  KeyboardAvoidingView,
  Platform,
  ScrollView
} from 'react-native'
import React, { useEffect, useState, useMemo } from 'react'
import { Ionicons } from "@expo/vector-icons";
import { MealLog } from "@/services/mealService";
import clsx from "clsx";

interface LogModalProps {
  isVisible: boolean;
  onClose: () => void;
  onSubmit: (name: string, weight: number) => void;
  log: MealLog | null;
}

const LogModal = ({ isVisible, onClose, onSubmit, log }: LogModalProps) => {
  const [name, setName] = useState('');
  const [weightStr, setWeightStr] = useState('');

  const baseValues = useMemo(() => {
    if (!log || log.weight === 0) return { cals: 0, p: 0, f: 0, c: 0 };
    return {
      cals: log.calories / log.weight,
      p: log.proteins / log.weight,
      f: log.fats / log.weight,
      c: log.carbs / log.weight,
    };
  }, [log]);

  useEffect(() => {
    if (log) {
      setName(log.name);
      setWeightStr(log.weight.toString());
    }
  }, [log, isVisible]);

  const currentWeight = parseFloat(weightStr) || 0;

  const displayValues = {
    calories: Math.round(baseValues.cals * currentWeight),
    proteins: (baseValues.p * currentWeight).toFixed(1),
    fats: (baseValues.f * currentWeight).toFixed(1),
    carbs: (baseValues.c * currentWeight).toFixed(1),
  };

  const handleSave = () => {
    const finalWeight = parseFloat(weightStr);
    if (finalWeight > 0 && name.trim().length > 0) {
      onSubmit(name, finalWeight);
      onClose();
    }
  };

  if (!log) return null;

  return (
    <Modal animationType="slide" visible={isVisible} presentationStyle="pageSheet" onRequestClose={onClose}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
        className="flex-1 bg-white dark:bg-dark-900"
      >
        <View className="flex-row justify-between items-center p-4 border-b border-light-200 dark:border-dark-800">
          <Text className="text-xl font-bold dark:text-white">Edit Log</Text>
          <Pressable onPress={onClose} className="p-2 bg-light-100 dark:bg-dark-800 rounded-full">
            <Ionicons name="close" size={24} color="gray" />
          </Pressable>
        </View>

        <ScrollView className="flex-1 px-6 pt-6" keyboardShouldPersistTaps="handled">

          <View className="items-center mb-8">
            <Text className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-2">
              Quantity (g)
            </Text>
            <View className="flex-row items-end">
              <TextInput
                value={weightStr}
                onChangeText={setWeightStr}
                keyboardType="numeric"
                placeholder="0"
                autoFocus={true}
                selectTextOnFocus={true}
                className="text-6xl font-extrabold text-primary border-b-2 border-transparent focus:border-primary min-w-[100px] text-center p-0"
              />
              <Text className="text-xl text-gray-400 font-bold mb-3 ml-2">g</Text>
            </View>
          </View>

          <View className="mb-8">
            <Text className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-2">
              Product Name
            </Text>
            <TextInput
              value={name}
              onChangeText={setName}
              placeholder="e.g. Banana"
              className="w-full bg-light-50 dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-4 py-4 text-lg font-semibold text-dark-900 dark:text-white"
            />
          </View>

          <View className="mb-8">
            <Text className="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">
              Macros
            </Text>

            <View className="flex-row gap-3">
              <View className="flex-1 bg-light-50 dark:bg-dark-800 p-3 rounded-xl border border-light-200 dark:border-dark-700 items-center">
                <Text className="text-2xl font-black text-dark-900 dark:text-white">
                  {displayValues.calories}
                </Text>
                <Text className="text-xs font-bold text-gray-400 uppercase">kcal</Text>
              </View>

              <View className="flex-1 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-xl border border-blue-100 dark:border-blue-900/30 items-center">
                <Text className="text-lg font-bold text-blue-700 dark:text-blue-400">
                  {displayValues.proteins}g
                </Text>
                <Text className="text-[10px] font-black text-blue-400 uppercase mt-1">Proteins</Text>
              </View>

              <View className="flex-1 bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-xl border border-yellow-100 dark:border-yellow-900/30 items-center">
                <Text className="text-lg font-bold text-yellow-700 dark:text-yellow-400">
                  {displayValues.fats}g
                </Text>
                <Text className="text-[10px] font-black text-yellow-500 uppercase mt-1">Fats</Text>
              </View>

              <View className="flex-1 bg-orange-50 dark:bg-orange-900/20 p-3 rounded-xl border border-orange-100 dark:border-orange-900/30 items-center">
                <Text className="text-lg font-bold text-orange-700 dark:text-orange-400">
                  {displayValues.carbs}g
                </Text>
                <Text className="text-[10px] font-black text-orange-500 uppercase mt-1">Carbs</Text>
              </View>
            </View>
          </View>
        </ScrollView>

        <View className="p-4 border-t border-light-200 dark:border-dark-800 bg-white dark:bg-dark-900">
          <Pressable
            onPress={handleSave}
            disabled={!name || !weightStr}
            className={clsx(
              "w-full py-4 rounded-2xl items-center shadow-sm",
              (!name || !weightStr) ? "bg-gray-300 dark:bg-dark-700" : "bg-primary active:opacity-90"
            )}
          >
            <Text className="text-white font-bold text-lg">Save Changes</Text>
          </Pressable>
        </View>

      </KeyboardAvoidingView>
    </Modal>
  )
}

export default LogModal