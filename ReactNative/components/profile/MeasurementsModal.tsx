import React from "react";
import { View, Text, Modal, FlatList, Pressable } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { Measurement } from "@/services/MeasurementsService";

interface MeasurementsModalProps {
  visible: boolean;
  onClose: () => void;
  measurements: Measurement[];
  onDelete: (id: number) => void;
}

const MeasurementsModal = ({ visible, onClose, measurements, onDelete }: MeasurementsModalProps) => {

  const renderStat = (label: string, value: number | null | undefined) => {
    if (!value) return null;

    return (
      <View className="bg-light-100 dark:bg-dark-700 px-2 py-2 rounded-lg mb-2 mr-2 min-w-[70px] items-center border border-light-200 dark:border-dark-600 flex-grow">
        <Text className="text-sm font-black text-dark-900 dark:text-white">
          {value}
        </Text>
        <Text className="text-[9px] font-bold text-gray-400 uppercase tracking-tighter">
          {label}
        </Text>
      </View>
    );
  };

  return (
    <Modal
      visible={visible}
      onRequestClose={onClose}
      animationType="slide"
      presentationStyle="pageSheet"
    >
      <View className="flex-1 bg-light-100 dark:bg-dark-900">

        <View className="flex-row justify-between items-center p-5 border-b border-light-200 dark:border-dark-700 bg-white dark:bg-dark-900">
          <Text className="text-xl font-black text-dark-900 dark:text-light-100">
            Measurements Log
          </Text>
          <Pressable
            onPress={onClose}
            className="w-10 h-10 items-center justify-center bg-light-200 dark:bg-dark-800 rounded-full"
          >
            <Ionicons name="close" size={24} color="#9ca3af" />
          </Pressable>
        </View>

        <FlatList<Measurement>
          data={measurements}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={{ padding: 20, paddingBottom: 50 }}
          renderItem={({ item }) => (
            <View className="bg-white dark:bg-dark-800 p-4 mb-4 rounded-2xl shadow-sm border border-light-200 dark:border-dark-700">

              <View className="flex-row justify-between items-center mb-4 border-b border-light-100 dark:border-dark-700 pb-3">
                <View className="flex-row items-center gap-2">
                   <Ionicons name="calendar" size={18} color="#6366f1" />
                   <Text className="text-base font-bold text-dark-900 dark:text-white opacity-80">
                     {item.date}
                   </Text>
                </View>

                <Pressable
                  onPress={() => onDelete(item.id)}
                  className="w-8 h-8 items-center justify-center bg-red-50 dark:bg-red-900/20 rounded-lg"
                >
                  <Ionicons name="trash-outline" size={18} color="#ef4444" />
                </Pressable>
              </View>

              <View className="flex-row flex-wrap">
                 {item.weight && (
                    <View className="bg-primary/10 px-3 py-2 rounded-lg mb-2 mr-2 min-w-[70px] items-center border border-primary/20 flex-grow">
                        <Text className="text-sm font-black text-primary">
                          {item.weight.weight}
                        </Text>
                        <Text className="text-[9px] font-bold text-primary/60 uppercase">
                          KG
                        </Text>
                    </View>
                 )}

                 {renderStat("Neck", item.neck)}
                 {renderStat("Chest", item.chest)}
                 {renderStat("Biceps", item.biceps)}
                 {renderStat("Waist", item.waist)}
                 {renderStat("Hips", item.hips)}
                 {renderStat("Thighs", item.thighs)}
                 {renderStat("Calves", item.calves)}
              </View>

            </View>
          )}
          ListEmptyComponent={
            <View className="items-center justify-center mt-20 opacity-50">
                <Ionicons name="body-outline" size={48} color="gray" />
                <Text className="text-gray-400 mt-4 font-bold">No measurements yet.</Text>
            </View>
          }
        />
      </View>
    </Modal>
  );
};

export default MeasurementsModal;