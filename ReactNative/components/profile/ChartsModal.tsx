import { View, Text, Modal, FlatList, Pressable, TouchableOpacity } from 'react-native';
import React, { useMemo, useState } from 'react';
import { LineChart } from "react-native-gifted-charts";
import { Weight } from "@/services/weightService";
import { Measurement } from "@/services/MeasurementsService";

const formatDateLabel = (dateString: string) => {
  const date = new Date(dateString);
  return `${date.getDate()}.${date.getMonth() + 1}`;
};

interface ChartsModalProps {
  visible: boolean;
  onClose: () => void;
  weights: Weight[];
  measurements: Measurement[];
}

const MEASUREMENT_TYPES = [
  "weight",
  "neck",
  "chest",
  "biceps",
  "waist",
  "hips",
  "thighs",
  "calves",
];

const ChartsModal = ({ visible, onClose, weights, measurements }: ChartsModalProps) => {
  const [selectedMeasurement, setSelectedMeasurement] = useState("weight");

  const chartData = useMemo(() => {
    let rawData: any[] = [];

    if (selectedMeasurement === "weight") {
      rawData = weights;
    } else {
      rawData = measurements;
    }

    const processedData = rawData
      .map((item) => {
        let value: number | null = 0;

        if (selectedMeasurement === "weight") {
           value = item.weight;
        } else {
           value = (item as Measurement)[selectedMeasurement as keyof Measurement] as number | null;
        }

        return {
          value: value,
          date: item.date,
          label: formatDateLabel(item.date),
          dataPointText: value?.toString(),
          dataPointColor: '#6366f1',
          textColor: '#6366f1',
          textShiftY: -10,
          textFontSize: 10,
        };
      })
      .filter((item) => item.value !== null && item.value > 0)
      .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    return processedData;
  }, [selectedMeasurement, weights, measurements]);

  return (
    <Modal visible={visible} animationType="slide" onRequestClose={onClose}>
      <View className="flex-1 bg-white dark:bg-slate-900 pt-12">

        <View className="px-4 mb-6 flex-row justify-between items-center">
          <Text className="text-2xl font-bold text-slate-800 dark:text-white capitalize">
            {selectedMeasurement} Progress
          </Text>
          <TouchableOpacity onPress={onClose} className="p-2 bg-slate-100 dark:bg-slate-800 rounded-full">
            <Text className="text-slate-500 dark:text-slate-300 font-bold">✕</Text>
          </TouchableOpacity>
        </View>

        <View className="mb-8">
          <FlatList
            horizontal
            data={MEASUREMENT_TYPES}
            keyExtractor={(item) => item}
            showsHorizontalScrollIndicator={false}
            contentContainerStyle={{ paddingHorizontal: 16, gap: 8 }}
            renderItem={({ item }) => {
              const isSelected = selectedMeasurement === item;
              return (
                <Pressable
                  onPress={() => setSelectedMeasurement(item)}
                  className={`px-4 py-2 rounded-full border ${
                    isSelected
                      ? "bg-indigo-500 border-indigo-500"
                      : "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                  }`}
                >
                  <Text
                    className={`font-medium capitalize ${
                      isSelected
                        ? "text-white"
                        : "text-slate-700 dark:text-slate-300"
                    }`}
                  >
                    {item}
                  </Text>
                </Pressable>
              );
            }}
          />
        </View>

        {/* Wykres */}
        <View className="items-center justify-center px-2">
            {chartData.length > 1 ? (
              <LineChart
                data={chartData}
                color="#6366f1"
                thickness={3}
                dataPointsColor="#6366f1"
                startFillColor="rgba(99, 102, 241, 0.3)"
                endFillColor="rgba(99, 102, 241, 0.01)"
                startOpacity={0.9}
                endOpacity={0.2}
                areaChart
                curved
                isAnimated
                animationDuration={1200}
                hideRules={false}
                rulesColor="#E5E7EB"
                xAxisLabelTextStyle={{color: 'gray', fontSize: 10}}
                yAxisTextStyle={{color: 'gray', fontSize: 10}}
                yAxisOffset={chartData.reduce((min, p) => p.value < min ? p.value : min, chartData[0].value) - 5}
                noOfSections={4}
                width={300}
                height={250}
                spacing={40}
              />
            ) : (
              <View className="h-64 justify-center items-center">
                <Text className="text-slate-400">
                  Not enough data to show chart (min. 2 entries)
                </Text>
              </View>
            )}
        </View>

      </View>
    </Modal>
  );
};

export default ChartsModal;