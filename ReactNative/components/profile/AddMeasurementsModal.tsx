import React, { useState, useEffect } from 'react';
import { View, Text, Modal, TextInput, Pressable, ScrollView, Switch, KeyboardAvoidingView, Platform } from 'react-native';
import { Ionicons } from "@expo/vector-icons";
import { WeightCreate } from "@/services/weightService";
import { MeasurementCreate } from "@/services/MeasurementsService";
import Toast from "react-native-toast-message";

interface AddMeasurementsModalProps {
  visible: boolean;
  onClose: () => void;
  onWeightSubmit: (weight: WeightCreate) => void;
  onMeasurementSubmit: (measurement: MeasurementCreate) => void;
}

const AddMeasurementsModal = ({ visible, onClose, onWeightSubmit, onMeasurementSubmit }: AddMeasurementsModalProps) => {
  const [isOnlyWeightSelected, setIsOnlyWeightSelected] = useState(false);

  const [weight, setWeight] = useState('');
  const [neck, setNeck] = useState('');
  const [biceps, setBiceps] = useState('');
  const [chest, setChest] = useState('');
  const [waist, setWaist] = useState('');
  const [hips, setHips] = useState('');
  const [thighs, setThighs] = useState('');
  const [calves, setCalves] = useState('');

  useEffect(() => {
    if (visible) {
        setWeight('');
        setNeck('');
        setBiceps('');
        setChest('');
        setWaist('');
        setHips('');
        setThighs('');
        setCalves('');
        setIsOnlyWeightSelected(false);
    }
  }, [visible]);

  const isFormValid = () => {
    if (isOnlyWeightSelected) {
        return weight.length > 0;
    }
    return weight.length > 0 || neck || biceps || chest || waist || hips || thighs || calves;
  };

  const handleSave = () => {
    const parse = (val: string) => val ? parseFloat(val.replace(',', '.')) : null;

    const weightValue = parse(weight);

    try {
      if (isOnlyWeightSelected) {
        if (weightValue === null) {
            Toast.show({type: 'error', text1: 'Weight is required'});
            return;
        }
        onWeightSubmit({ weight: weightValue });
      } else {

        const measurementData: MeasurementCreate = {
          weight: weightValue ? { weight: weightValue } : null,
          neck: parse(neck),
          biceps: parse(biceps),
          chest: parse(chest),
          waist: parse(waist),
          hips: parse(hips),
          thighs: parse(thighs),
          calves: parse(calves)
        };
        onMeasurementSubmit(measurementData);
      }
      onClose();
    } catch (e) {
      console.error(e);
    }
  };

  const renderInput = (label: string, value: string, setter: (t: string) => void) => (
    <View className="w-[48%] mb-4">
        <Text className="text-xs font-bold text-gray-500 uppercase mb-2 ml-1">{label} (cm)</Text>
        <View className="bg-white dark:bg-dark-800 border border-light-200 dark:border-dark-700 rounded-xl px-4 py-2">
            <TextInput
                value={value}
                onChangeText={setter}
                keyboardType="numeric"
                placeholder="0.0"
                placeholderTextColor="#9ca3af"
                className="text-lg font-bold text-dark-900 dark:text-white"
            />
        </View>
    </View>
  );

  return (
    <Modal
      visible={visible}
      onRequestClose={onClose}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        className="flex-1 bg-light-100 dark:bg-dark-900"
      >
        <View className="flex-row justify-between items-center p-5 border-b border-light-200 dark:border-dark-700 bg-white dark:bg-dark-900">
          <Text className="text-xl font-black text-dark-900 dark:text-light-100">
            Add Measurement
          </Text>
          <Pressable onPress={onClose} className="w-10 h-10 items-center justify-center bg-light-200 dark:bg-dark-800 rounded-full">
            <Ionicons name="close" size={24} color="#9ca3af" />
          </Pressable>
        </View>

        <ScrollView contentContainerStyle={{ padding: 24 }}>

            <View className="bg-white dark:bg-dark-800 p-4 rounded-3xl border border-light-200 dark:border-dark-700 mb-6 shadow-sm">
                <Text className="text-sm font-bold text-gray-500 uppercase mb-2 ml-1">Current Weight (kg)</Text>
                <View className="flex-row items-center justify-between">
                    <View className="flex-1 mr-4 bg-light-100 dark:bg-dark-900 rounded-2xl px-4 py-2 border border-light-200 dark:border-dark-600">
                        <TextInput
                            value={weight}
                            onChangeText={setWeight}
                            keyboardType="numeric"
                            placeholder="0.0"
                            placeholderTextColor="#9ca3af"
                            className="text-3xl font-black text-primary"
                            autoFocus={true}
                        />
                    </View>
                    <View className="w-12 h-12 bg-primary/10 rounded-full items-center justify-center">
                        <Ionicons name="scale" size={24} color="#6366f1" />
                    </View>
                </View>

                <View className="flex-row items-center justify-between pt-2 mt-4 border-t border-light-100 dark:border-dark-700">
                    <View className="flex-row items-center">
                        <Ionicons name="filter-outline" size={20} color={isOnlyWeightSelected ? "#6366f1" : "gray"} />
                        <Text className={`ml-2 font-bold ${isOnlyWeightSelected ? 'text-primary' : 'text-gray-500'}`}>
                            Log Weight Only
                        </Text>
                    </View>
                    <Switch
                        value={isOnlyWeightSelected}
                        onValueChange={setIsOnlyWeightSelected}
                        trackColor={{ false: "#e5e7eb", true: "#6366f1" }}
                        thumbColor={"white"}
                    />
                </View>
            </View>

            {!isOnlyWeightSelected && (
                <View>
                    <Text className="text-sm font-bold text-gray-400 uppercase mb-4 ml-1">Body Circumferences</Text>

                    <View className="flex-row flex-wrap justify-between">
                        {renderInput("Neck", neck, setNeck)}
                        {renderInput("Chest", chest, setChest)}
                        {renderInput("Biceps", biceps, setBiceps)}
                        {renderInput("Waist", waist, setWaist)}
                        {renderInput("Hips", hips, setHips)}
                        {renderInput("Thighs", thighs, setThighs)}
                        {renderInput("Calves", calves, setCalves)}
                        <View className="w-[48%]" />
                    </View>
                </View>
            )}

            <View className="h-24" />
        </ScrollView>

        <View className="p-5 border-t border-light-200 dark:border-dark-700 bg-white dark:bg-dark-900 pb-10">
            <Pressable
                onPress={handleSave}
                disabled={!isFormValid()}
                className={`w-full py-4 rounded-2xl items-center justify-center flex-row shadow-sm
                    ${isFormValid() ? 'bg-primary' : 'bg-gray-200 dark:bg-dark-700'}
                `}
            >
                <Ionicons name="checkmark-circle" size={24} color={isFormValid() ? "white" : "#9ca3af"} style={{marginRight: 8}} />
                <Text className={`text-lg font-bold ${isFormValid() ? 'text-white' : 'text-gray-400'}`}>
                    Save Record
                </Text>
            </Pressable>
        </View>

      </KeyboardAvoidingView>
    </Modal>
  );
};

export default AddMeasurementsModal;