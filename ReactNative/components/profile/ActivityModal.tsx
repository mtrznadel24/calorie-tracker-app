import {
  View,
  Text,
  Modal,
  Pressable,
  ActivityIndicator,
  TextInput,
  Keyboard
} from 'react-native';
import React, { useEffect, useState } from 'react';
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import clsx from "clsx";
import { KeyboardAwareScrollView } from "react-native-keyboard-aware-scroll-view";
import Toast from "react-native-toast-message";

interface RateModalProps {
  visible: boolean;
  currentLevel?: number;
  onClose: () => void;
  onSave: (level: number) => Promise<void>;
}

const ACTIVITY_LEVELS = [
  { id: 1.2, label: "Sedentary", desc: "Little or no exercise, desk job", icon: "chair-school" },
  { id: 1.375, label: "Lightly Active", desc: "Light exercise 1-3 days/week", icon: "walk" },
  { id: 1.55, label: "Moderately Active", desc: "Moderate exercise 3-5 days/week", icon: "run" },
  { id: 1.725, label: "Very Active", desc: "Hard exercise 6-7 days/week", icon: "bike" },
  { id: 1.9, label: "Extra Active", desc: "Very hard exercise, physical job", icon: "fire" },
];

const ActivityModal = ({ visible, currentLevel, onClose, onSave }: RateModalProps) => {
  const [selectedLevel, setSelectedLevel] = useState<number | null>(null);

  const [isTextInput, setIsTextInput] = useState<boolean>(false);
  const [customValue, setCustomValue] = useState<string>("");

  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (visible) {
      const knownIds = ACTIVITY_LEVELS.map(l => l.id);
      const isKnown = currentLevel ? knownIds.includes(currentLevel) : false;

      if (currentLevel && !isKnown) {
        setIsTextInput(true);
        setCustomValue(currentLevel.toString());
        setSelectedLevel(null);
      } else {
        setIsTextInput(false);
        setSelectedLevel(currentLevel || 1.2);
        setCustomValue("");
      }
      setIsSaving(false);
    }
  }, [visible, currentLevel]);

  const handleSave = async () => {
    if (isSaving) return;

    let finalValue: number;

    if (isTextInput) {
      finalValue = parseFloat(customValue.replace(',', '.'));
      if (isNaN(finalValue) || finalValue < 1.0 || finalValue > 3.0) {
        Toast.show({
          type: 'error',
          text1: 'Invalid Value',
          text2: 'Activity level must be a number between 1.0 and 3.0'
        });
        return;
      }
    } else {
      if (!selectedLevel) return;
      finalValue = selectedLevel;
    }

    setIsSaving(true);
    await onSave(finalValue);
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
      <View className="flex-1 bg-black/60 justify-end sm:justify-center">

        <View className="bg-light-50 dark:bg-dark-900 h-[95%] rounded-t-3xl overflow-hidden">

            <View className="p-4 flex-row justify-end">
                <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-800 rounded-full">
                  <Ionicons name="close" size={24} color="#9CA3AF" />
                </Pressable>
            </View>

            <KeyboardAwareScrollView contentContainerStyle={{ paddingHorizontal: 24, paddingBottom: 40 }}>

              <Text className="text-2xl font-bold text-dark-900 dark:text-light-100 mb-2 text-center">
                Activity Level
              </Text>
              <Text className="text-sm text-dark-700 dark:text-gray-400 mb-8 text-center">
                Select the level that best matches your daily routine or enter a custom value.
              </Text>

              <View className="gap-y-3 mb-6">
                {ACTIVITY_LEVELS.map((level) => (
                  <Pressable
                    key={level.id}
                    onPress={() => {
                      setSelectedLevel(level.id);
                      setIsTextInput(false);
                      Keyboard.dismiss();
                    }}
                    className={clsx(
                      "flex-row items-center p-4 rounded-2xl border-2",
                      selectedLevel === level.id && !isTextInput
                        ? "border-primary bg-primary/5 dark:bg-primary/10"
                        : "border-light-200 dark:border-dark-700 bg-light-100 dark:bg-dark-800"
                    )}
                  >
                    <View className={clsx(
                      "w-12 h-12 rounded-full items-center justify-center mr-4",
                      selectedLevel === level.id && !isTextInput ? "bg-primary" : "bg-light-300 dark:bg-dark-600"
                    )}>
                      <MaterialCommunityIcons
                        name={level.icon as any}
                        size={24}
                        color={selectedLevel === level.id && !isTextInput ? "white" : "#9CA3AF"}
                      />
                    </View>

                    <View className="flex-1">
                      <Text className={clsx(
                        "font-bold text-lg",
                        selectedLevel === level.id && !isTextInput ? "text-primary" : "text-dark-900 dark:text-light-100"
                      )}>
                        {level.label}
                      </Text>
                      <Text className="text-xs text-dark-600 dark:text-gray-400">
                        {level.id} - {level.desc}
                      </Text>
                    </View>

                    {selectedLevel === level.id && !isTextInput && (
                      <MaterialCommunityIcons name="check-circle" size={24} color="#3b82f6" />
                    )}
                  </Pressable>
                ))}
              </View>

              <Pressable
                onPress={() => setIsTextInput(true)}
                className={clsx(
                  "flex-row items-center p-4 rounded-2xl border-2 mb-4",
                  isTextInput
                    ? "border-primary bg-primary/5 dark:bg-primary/10"
                    : "border-light-200 dark:border-dark-700 bg-light-100 dark:bg-dark-800"
                )}
              >
                  <View className={clsx(
                      "w-12 h-12 rounded-full items-center justify-center mr-4",
                      isTextInput ? "bg-primary" : "bg-light-300 dark:bg-dark-600"
                    )}>
                      <MaterialCommunityIcons
                        name="tune"
                        size={24}
                        color={isTextInput ? "white" : "#9CA3AF"}
                      />
                  </View>

                  <View className="flex-1">
                      <Text className={clsx(
                        "font-bold text-lg mb-1",
                        isTextInput ? "text-primary" : "text-dark-900 dark:text-light-100"
                      )}>
                        Custom Value
                      </Text>
                      <TextInput
                        value={customValue}
                        onChangeText={(text) => {
                          setCustomValue(text);
                          setIsTextInput(true);
                          setSelectedLevel(null);
                        }}
                        onFocus={() => {
                           setIsTextInput(true);
                           setSelectedLevel(null);
                        }}
                        placeholder="e.g. 1.45"
                        placeholderTextColor="#9CA3AF"
                        keyboardType="numeric"
                        className={clsx(
                          "text-xl font-semibold border-b py-1",
                          isTextInput
                            ? "text-dark-900 dark:text-white border-primary"
                            : "text-gray-400 border-transparent"
                        )}
                      />
                  </View>

                   {isTextInput && (
                      <MaterialCommunityIcons name="check-circle" size={24} color="#3b82f6" />
                    )}
              </Pressable>

              <View className="mt-4">
                <Pressable
                  onPress={handleSave}
                  disabled={isSaving}
                  className={`w-full py-4 rounded-2xl items-center justify-center shadow-sm
                    ${!isSaving && (selectedLevel || (isTextInput && customValue))
                      ? "bg-primary active:opacity-90" 
                      : "bg-gray-300 dark:bg-dark-700 opacity-50"
                    }`}
                >
                  {isSaving ? (
                     <ActivityIndicator color="#fff" />
                  ) : (
                     <Text className="text-white font-bold text-lg">Save Changes</Text>
                  )}
                </Pressable>
              </View>
            </KeyboardAwareScrollView>
        </View>
      </View>
    </Modal>
  );
};

export default ActivityModal;