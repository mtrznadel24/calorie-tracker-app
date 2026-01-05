import {
  View,
  Text,
  Modal,
  Pressable,
  TextInput,
  KeyboardAvoidingView,
  Platform,
  TouchableWithoutFeedback,
  Keyboard
} from 'react-native';
import React, { useEffect, useState } from 'react';
import { Ionicons } from "@expo/vector-icons";
import Toast from "react-native-toast-message";
import clsx from "clsx";

interface RateModalProps {
  visible: boolean;
  currentRate?: number;
  onClose: () => void;
  onSave: (rate: number) => Promise<void>;
}

type PlanType = "Loss" | "Maintain" | "Gain";

const RateModal = ({ visible, currentRate, onClose, onSave }: RateModalProps) => {
  const [plan, setPlan] = useState<PlanType>("Maintain");
  const [rateStr, setRateStr] = useState("0.5");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (visible) {
      if (!currentRate || currentRate === 0) {
        setPlan("Maintain");
        setRateStr("0");
      } else if (currentRate > 0) {
        setPlan("Gain");
        setRateStr(currentRate.toString());
      } else {
        setPlan("Loss");
        setRateStr(Math.abs(currentRate).toString());
      }
      setIsSaving(false);
    }
  }, [visible, currentRate]);

  const handleAdjustRate = (adjustment: number) => {
    const currentVal = parseFloat(rateStr) || 0;
    const newVal = currentVal + adjustment;

    if (newVal < 0.1) {
       setRateStr("0.1");
       return;
    }
    if (newVal > 1.5) {
       Toast.show({ type: 'info', text1: 'Limit reached', text2: 'Maximum recommended rate is 1.5kg/week' });
       setRateStr("1.5");
       return;
    }

    setRateStr(newVal.toFixed(1));
  };

  const handleSave = async () => {
    if (isSaving) return;

    let finalRate = 0;

    if (plan === "Maintain") {
      finalRate = 0;
    } else {
      const parsed = parseFloat(rateStr.replace(',', '.'));

      if (isNaN(parsed) || parsed <= 0) {
        Toast.show({ type: 'error', text1: 'Invalid rate', text2: 'Please enter a valid number greater than 0' });
        return;
      }

      finalRate = plan === "Loss" ? -parsed : parsed;
    }

    setIsSaving(true);
    await onSave(finalRate);
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
                  Target Goal
                </Text>
                <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-700 rounded-full">
                  <Ionicons name="close" size={20} color="#9CA3AF" />
                </Pressable>
              </View>

              <View className="flex-row bg-light-200 dark:bg-dark-700 p-1 rounded-xl mb-8">
                {(["Loss", "Maintain", "Gain"] as PlanType[]).map((type) => (
                  <Pressable
                    key={type}
                    onPress={() => {
                      setPlan(type);
                      if (type !== "Maintain" && (rateStr === "0" || !rateStr)) {
                        setRateStr("0.5");
                      }
                    }}
                    className={clsx(
                      "flex-1 py-2 items-center rounded-lg",
                      plan === type
                        ? "bg-white dark:bg-dark-600"
                        : "bg-transparent"
                    )}
                  >
                    <Text className={clsx(
                      "font-bold text-sm",
                      plan === type ? "text-primary" : "text-gray-500"
                    )}>
                      {type}
                    </Text>
                  </Pressable>
                ))}
              </View>

              <View className="items-center mb-8 h-32 justify-center">
                {plan === "Maintain" ? (
                  <View className="items-center">
                    <Ionicons name="checkmark-circle-outline" size={48} color="#10b981" />
                    <Text className="text-dark-900 dark:text-light-100 font-bold text-lg mt-2">
                      Maintain Weight
                    </Text>
                    <Text className="text-gray-500 text-xs">Target change: 0 kg / week</Text>
                  </View>
                ) : (
                  <>
                    <View className="flex-row items-center justify-between w-full px-4">
                      <Pressable
                        onPress={() => handleAdjustRate(-0.1)}
                        hitSlop={20}
                        className="w-12 h-12 bg-primary rounded-full items-center justify-center active:opacity-70"
                      >
                        <Ionicons name="remove" size={24} color="#9CA3AF" />
                      </Pressable>

                      <View className="items-center">
                        <View className="flex-row items-baseline">
                          <TextInput
                            value={rateStr}
                            onChangeText={setRateStr}
                            keyboardType="numeric"
                            className="text-5xl font-black text-dark-900 dark:text-white text-center min-w-[80px]"
                            maxLength={4}
                          />
                          <Text className="text-lg font-bold text-gray-500 ml-1">kg</Text>
                        </View>
                        <Text className="text-xs font-bold text-gray-400 uppercase tracking-widest">
                          Per Week
                        </Text>
                      </View>

                      <Pressable
                        onPress={() => handleAdjustRate(0.1)}
                        hitSlop={20}
                        className="w-12 h-12 bg-primary rounded-full items-center justify-center active:opacity-70 shadow-sm"
                      >
                        <Ionicons name="add" size={24} color="white" />
                      </Pressable>
                    </View>

                    <Text className="text-gray-400 text-[10px] mt-4 text-center px-4">
                       Recommended rate is 0.1 - 0.5 kg per week.
                    </Text>
                  </>
                )}
              </View>

              <View className="gap-3">
                <Pressable
                  onPress={handleSave}
                  disabled={isSaving || (plan !== "Maintain" && !rateStr)}
                  className={`w-full py-4 rounded-2xl items-center justify-center shadow-sm
                    ${!isSaving
                      ? "bg-primary active:opacity-90" 
                      : "bg-gray-300 dark:bg-dark-700 opacity-50"
                    }`}
                >
                  {isSaving ? (
                     <Text className="text-lg font-bold text-white">Saving...</Text>
                  ) : (
                     <Text className="text-lg font-bold text-white">Save Goal</Text>
                  )}
                </Pressable>
              </View>

            </KeyboardAvoidingView>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
};

export default RateModal;