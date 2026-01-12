
import {Weight} from "@/services/weightService";
import {FlatList, Modal, Pressable, View, Text} from "react-native";
import {Ionicons} from "@expo/vector-icons";

interface WeightsModalProps {
  visible: boolean,
  onClose: () => void
  weights: Weight[],
  onDelete: (id: number) => void
}

const WeightsModal = ({visible, onClose, weights, onDelete}: WeightsModalProps) => {

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
            Weight History
          </Text>
          <Pressable
            onPress={onClose}
            className="w-10 h-10 items-center justify-center bg-light-200 dark:bg-dark-800 rounded-full"
          >
            <Ionicons name="close" size={24} color="#9ca3af" />
          </Pressable>
        </View>

        <FlatList<Weight>
          data={weights}
          keyExtractor={(item) => item.id.toString()}
          contentContainerStyle={{ padding: 20, paddingBottom: 50 }}
          renderItem={({ item }) => (
            <View className="flex-row justify-between items-center bg-white dark:bg-dark-800 p-4 mb-3 rounded-2xl shadow-sm border border-light-200 dark:border-dark-700">

              <View className="flex-row items-center gap-4">
                <View className="w-12 h-12 rounded-2xl bg-primary/10 items-center justify-center">
                   <Ionicons name="calendar-outline" size={22} color="#6366f1" />
                </View>

                <View>
                  <Text className="text-xl font-black text-dark-900 dark:text-white">
                    {item.weight} <Text className="text-sm font-normal text-gray-500">kg</Text>
                  </Text>
                  <Text className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                    {item.date}
                  </Text>
                </View>
              </View>

              <Pressable
                onPress={() => onDelete(item.id)}
                className="w-10 h-10 items-center justify-center bg-red-50 dark:bg-red-900/20 rounded-xl"
              >
                <Ionicons name="trash-outline" size={20} color="#ef4444" />
              </Pressable>

            </View>
          )}
          ListEmptyComponent={
            <View className="items-center justify-center mt-20 opacity-50">
                <Ionicons name="folder-open-outline" size={48} color="gray" />
                <Text className="text-gray-400 mt-4 font-bold">No history yet.</Text>
            </View>
          }
        />
      </View>
    </Modal>
  );
}

export default WeightsModal