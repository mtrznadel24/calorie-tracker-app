import {
  View,
  Text,
  Modal,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  TextInput,
  ActivityIndicator
} from 'react-native'
import React, { useState, useEffect } from 'react'
import { Ionicons } from "@expo/vector-icons";

interface Props {
  name: string
  initialWeight: number
  isVisible: boolean
  isLoading?: boolean;
  onClose: () => void
  onSubmit: (weight: number) => void
}

const SetWeightModal = ({ name, initialWeight, isVisible, isLoading = false, onClose, onSubmit }: Props) => {
  const [weight, setWeight] = useState(initialWeight.toString());

  useEffect(() => {
    setWeight(initialWeight.toString());
  }, [initialWeight, isVisible]);

  const handleSubmit = () => {
    const parsedWeight = parseFloat(weight);
    if (!isNaN(parsedWeight) && parsedWeight > 0) {
      onSubmit(parsedWeight);
    }
  };

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={isVisible}
      onRequestClose={onClose}
    >
       <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} className="flex-1 bg-white dark:bg-dark-900 justify-center px-6">

          <Pressable onPress={onClose} className="absolute top-12 left-4 z-10 p-2 bg-light-100 dark:bg-dark-800 rounded-full">
              <Ionicons name="arrow-back" size={24} color="gray" />
          </Pressable>

          <View className="items-center w-full">
              <Text className="text-2xl font-bold mb-6 dark:text-white text-center">
                How much {name}?
              </Text>

              <View className="flex-row items-end justify-center gap-2 mb-10">
                  <TextInput
                      value={weight}
                      onChangeText={setWeight}
                      keyboardType="numeric"
                      autoFocus={true}
                      selectTextOnFocus={true}
                      placeholder="0"
                      className="text-6xl font-bold text-primary border-b-2 border-primary min-w-[100px] text-center dark:text-white"
                  />
                  <Text className="text-2xl text-gray-400 pb-4">g</Text>
              </View>

              <Pressable
                onPress={handleSubmit}
                disabled={!weight || isLoading}
                className={`w-full p-4 rounded-xl items-center ${(!weight || isLoading) ? 'bg-gray-300' : 'bg-primary'}`}
              >
                  {isLoading ? (
                    <ActivityIndicator color="white"/>
                  ) : (
                    <Text className="text-white font-bold text-lg">Add to meal logs</Text>
                  )}
              </Pressable>
          </View>
       </KeyboardAvoidingView>
    </Modal>
  );
}

export default SetWeightModal