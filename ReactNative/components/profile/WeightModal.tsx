import { View, Text, Modal, Pressable, TextInput, KeyboardAvoidingView, Platform, TouchableWithoutFeedback, Keyboard } from 'react-native';
import React, { useEffect, useState } from 'react';
import { Ionicons } from "@expo/vector-icons";
import Toast from "react-native-toast-message";

interface WeightModalProps {
  visible: boolean;
  currentWeight?: number;
  onClose: () => void;
  onSave: (weight: number) => Promise<void>;
}

const WeightModal = ({ visible, currentWeight, onClose, onSave }: WeightModalProps) => {
  const [weight, setWeight] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (visible) {
      setWeight(currentWeight ? currentWeight.toString() : "");
      setIsSaving(false);
    }
  }, [visible, currentWeight]);

  const handleSave = async () => {
    if (!weight || isSaving) return;

    const parsedWeight = parseFloat(weight.replace(',', '.'));

    if (isNaN(parsedWeight) || parsedWeight <= 0 || parsedWeight > 300) {
      Toast.show({
        type: 'error',
        text1: 'Error',
        text2: 'Weight should be between 0 and 300'
      });
      return;
    }

    setIsSaving(true);
    await onSave(parsedWeight);
    setIsSaving(false);
    onClose();
  };

  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="fade"
      onRequestClose={onClose}
    >
      <TouchableWithoutFeedback onPress={() => { Keyboard.dismiss(); onClose(); }}>
        <View className="flex-1 bg-black/60 justify-center px-6">
          <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
            <KeyboardAvoidingView
              behavior={Platform.OS === "ios" ? "padding" : "height"}
              className="bg-light-100 dark:bg-dark-800 rounded-3xl p-6 shadow-2xl border border-light-200 dark:border-dark-700"
            >

              <View className="flex-row justify-between items-center mb-6">
                <Text className="text-xl font-bold text-dark-900 dark:text-white">
                  Update Weight
                </Text>
                <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-700 rounded-full">
                  <Ionicons name="close" size={20} color="#9CA3AF" />
                </Pressable>
              </View>

              <View className="items-center mb-8">
                <View className="flex-row items-baseline">
                  <TextInput
                    value={weight}
                    onChangeText={setWeight}
                    keyboardType="numeric"
                    autoFocus={true}
                    placeholder="0.0"
                    placeholderTextColor="#6B7280"
                    className="text-6xl font-black text-primary text-center min-w-[120px]"
                    maxLength={5}
                  />
                  <Text className="text-xl font-bold text-gray-400 ml-2">kg</Text>
                </View>
                <Text className="text-xs text-gray-400 mt-2">
                  Enter your current body weight
                </Text>
              </View>

              {/* Przyciski */}
              <View className="gap-3">
                <Pressable
                  onPress={handleSave}
                  disabled={isSaving || !weight}
                  className={`w-full py-4 rounded-2xl items-center justify-center shadow-sm
                    ${!isSaving && weight
                      ? "bg-primary active:opacity-90" 
                      : "bg-gray-300 dark:bg-dark-700 opacity-50"
                    }`}
                >
                  {isSaving ? (
                     <Text className="text-lg font-bold text-white">Saving...</Text>
                  ) : (
                     <Text className="text-lg font-bold text-white">Save Weight</Text>
                  )}
                </Pressable>

                <Pressable
                  onPress={onClose}
                  disabled={isSaving}
                  className="w-full py-4 items-center justify-center active:opacity-60"
                >
                  <Text className="text-gray-500 font-semibold">Cancel</Text>
                </Pressable>
              </View>

            </KeyboardAvoidingView>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
};

export default WeightModal;