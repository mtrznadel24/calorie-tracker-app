import {View, Text, ScrollView, Alert} from 'react-native'
import React, {useEffect, useState} from 'react'
import {Ionicons} from "@expo/vector-icons";
import MenuButton from "@/components/profile/MenuButton";
import {useAuth} from "@/contexts/AuthContext";
import measurementsService, {Measurement, MeasurementCreate} from "@/services/MeasurementsService";
import WeightsModal from "@/components/profile/WeightsModal";
import MeasurementsModal from "@/components/profile/MeasurementsModal";
import weightService, {Weight, WeightCreate} from "@/services/weightService";
import Toast from "react-native-toast-message";
import AddMeasurementsModal from "@/components/profile/AddMeasurementsModal";
import ChartsModal from "@/components/profile/ChartsModal";

const MeasurementCard = ({ label, value, unit, icon, color }: any) => (
  <View className="w-[48%] bg-white dark:bg-dark-800 p-4 rounded-2xl border border-light-200 dark:border-dark-700 mb-4 shadow-sm relative overflow-hidden">
    <View className="absolute -right-4 -top-4 w-20 h-20 rounded-full opacity-5" style={{ backgroundColor: color }} />
    <View className="flex-row justify-between items-start mb-2">
      <View className="p-2 rounded-full bg-light-100 dark:bg-dark-700">
           <Ionicons name={icon} size={20} color={color} />
      </View>
      <Text className="text-3xl font-black text-dark-900 dark:text-white tracking-tight">
        {value ? value : "--"}<Text className="text-sm font-medium text-gray-400 ml-1">{unit}</Text>
      </Text>
    </View>
    <Text className="text-xs uppercase font-bold text-gray-400 mt-1 tracking-wider">
      {label}
    </Text>
  </View>
);

const MeasurementsScreen = () => {
  const { user, setUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [weights, setWeights] = useState<Weight[]>([]);
  const [measurements, setMeasurements] = useState<Measurement[]>([]);
  const [latestMeasurement, setLatestMeasurement] = useState<Measurement | null>(null);
  const [chartsModalVisible, setChartsModalVisible] = useState(false);
  const [weightsModalVisible, setWeightsModalVisible] = useState(false);
  const [measurementsModalVisible, setMeasurementsModalVisible] = useState(false);
  const [addMeasurementsModalVisible, setAddMeasurementsModalVisible] = useState(false);

  useEffect(() => {
    fetchWeights();
    fetchMeasurements();
  }, [])

  const fetchWeights = async () => {
    setIsLoading(false);
    try {
      const weights = await weightService.getUserWeights();
      setWeights(weights);
    } catch (e) {
      console.error(e)
      Toast.show({type: "error", text1: "Failed to fetch data"})
    } finally {
      setIsLoading(false);
    }
  }

  const fetchMeasurements = async () => {
    setIsLoading(true);
    try {
      const measurements = await measurementsService.getUserMeasurements();
      setMeasurements(measurements);
      setLatestMeasurement(measurements[0])
    } catch (e) {
      console.error(e);
      Toast.show({type: "error", text1: "Failed to fetch measurements"})
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteWeight = async (id: number) => {
    try {
      await weightService.deleteWeight(id);
      setWeights(prevWeights => {
          const newList = prevWeights.filter(w => w.id !== id);

          const newCurrentWeight = newList.length > 0 ? newList[0].weight : null;

          setUser(prevUser => ({
              ...prevUser!,
              current_weight: newCurrentWeight
          }));

          return newList;
      });
    } catch (e) {
      console.log(e);
      Toast.show({type: "error", text1: "Failed to delete weight"})
    }
  }

  const handleDeleteMeasurement = async (id: number) => {
    try {
      await measurementsService.deleteMeasurement(id);
      setMeasurements(measurements => {
        const newList = measurements.filter(measurement => measurement.id != id)
        const newMeasurement = newList.length > 0 ? newList[0] : null;
        setLatestMeasurement(newMeasurement);
        return newList;
      }
      );

    } catch (e) {
      console.log(e);
      Toast.show({type: "error", text1: "Failed to delete measurement"})
    }
  }

  const handleAddWeight = async (weight: WeightCreate) => {
    const today = new Date().toISOString().split('T')[0];
    const hasEntryToday = weights.length > 0 && weights[0].date === today;

    const saveNewData = async () => {
      try {
        const newWeight = await weightService.addWeight(weight);
        setWeights(weights => [newWeight, ...weights.filter(weight => weight.date !== newWeight.date)])
        setUser(user => ({...user, current_weight: newWeight.weight}))
        setMeasurements(prevMs => prevMs.map(m =>
        m.date === newWeight.date ? { ...m, weight: newWeight } : m
      ));
        Toast.show({type: "success", text1: "Weight added"})
      } catch (e) {
        console.error(e);
        Toast.show({type: "error", text1: "Failed to add weight"})
      }
    }

     if (hasEntryToday) {
      Alert.alert(
        "Entry Already Exists",
        "You have already added a weight today. Do you want to overwrite it with the new data?",
        [
          { text: "Cancel", style: "cancel" },
          { text: "Overwrite", onPress: () => saveNewData() }
        ]
      );
    } else {
      saveNewData()
    }

  }

  const handleAddMeasurement = async (measurement: MeasurementCreate) => {
    const today = new Date().toISOString().split('T')[0];
    const hasEntryToday = measurements.length > 0 && measurements[0].date === today;

    const saveNewData = async () => {
      try {
        const newMeasurement = await measurementsService.addMeasurement(measurement);
        setMeasurements(measurements => [newMeasurement, ...measurements.filter(m => m.date !== newMeasurement.date)]);
        setLatestMeasurement(newMeasurement)
        if (newMeasurement.weight) {
          setWeights(prevWeights => [
            newMeasurement.weight,
            ...prevWeights.filter(w => w.date !== newMeasurement.weight.date)
          ]);
          setUser(prev => ({...prev!, current_weight: newMeasurement.weight.weight}));
        }
        Toast.show({type: "success", text1: "Measurement added"})
      } catch (e) {
        console.error(e);
        Toast.show({type: "error", text1: "Failed to add measurement"})
      }
    }

    if (hasEntryToday) {
      Alert.alert(
        "Entry Already Exists",
        "You have already added a measurement today. Do you want to overwrite it with the new data?",
        [
          { text: "Cancel", style: "cancel" },
          { text: "Overwrite", onPress: () => saveNewData() }
        ]
      );
    } else {
      saveNewData()
    }
  }

  const bodyParts = [
    { label: "Neck", value: latestMeasurement?.neck, icon: "person-outline", color: "#6366f1" },
    { label: "Chest", value: latestMeasurement?.chest, icon: "shirt-outline", color: "#ec4899" },
    { label: "Biceps", value: latestMeasurement?.biceps, icon: "barbell-outline", color: "#8b5cf6" },
    { label: "Waist", value: latestMeasurement?.waist, icon: "hourglass-outline", color: "#f59e0b" },
    { label: "Hips", value: latestMeasurement?.hips, icon: "scan-outline", color: "#10b981" },
    { label: "Thighs", value: latestMeasurement?.thighs, icon: "flash-outline", color: "#3b82f6" },
    { label: "Calves", value: latestMeasurement?.calves, icon: "footsteps-outline", color: "#0ea5e9" },
  ];

  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-900">
      <ScrollView contentContainerStyle={{ padding: 24 }}>

        <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-4 ml-1">
          Latest Update: {latestMeasurement?.date || "No data"}
        </Text>

        <View className="flex-row flex-wrap justify-between">
            <View className="w-full bg-primary/10 dark:bg-primary/20 p-5 rounded-2xl border border-primary/20 mb-4 flex-row items-center justify-between">
                <View>
                    <Text className="text-gray-500 dark:text-primary/80 uppercase font-bold text-xs">Current Weight</Text>
                    <Text className="text-4xl font-black text-primary mt-1">
                        {user?.current_weight || "--"} <Text className="text-lg font-normal text-primary/60">kg</Text>
                    </Text>
                </View>
                <View className="w-12 h-12 rounded-full bg-primary items-center justify-center shadow-lg shadow-primary/40">
                    <Ionicons name="scale" size={24} color="white" />
                </View>
            </View>

            {bodyParts.map((item, index) => (
                <MeasurementCard
                    key={index}
                    label={item.label}
                    value={item.value}
                    unit="cm"
                    icon={item.icon}
                    color={item.color}
                />
            ))}
        </View>

        <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-4 ml-1 mt-4">
          Actions
        </Text>

        <View className="mb-8">
          <MenuButton
            title="Charts & Trends"
            icon="trending-up-outline"
            onPress={() => setChartsModalVisible(true)}
            color="#3b82f6"
          />
          <MenuButton
            title="Weight History"
            icon="calendar-number-outline"
            onPress={() => setWeightsModalVisible(true)}
            color="#10b981"
          />
          <MenuButton
            title="Measurements History"
            icon="clipboard-outline"
            onPress={() => setMeasurementsModalVisible(true)}
            color="#8b5cf6"
          />
          <MenuButton
            title="Add Measurements"
            icon="add-circle-outline"
            onPress={() => setAddMeasurementsModalVisible(true)}
            color="#f59e0b"
          />
        </View>

      </ScrollView>
      <ChartsModal
        visible={chartsModalVisible}
        onClose={() => setChartsModalVisible(false)}
        weights={weights}
        measurements={measurements}
      ></ChartsModal>
      <WeightsModal
        visible={weightsModalVisible}
        onClose={() => setWeightsModalVisible(false)}
        weights={weights}
        onDelete={handleDeleteWeight}
      ></WeightsModal>
      <MeasurementsModal
        visible={measurementsModalVisible}
        onClose={() => setMeasurementsModalVisible(false)}
        measurements={measurements}
        onDelete={handleDeleteMeasurement}
      ></MeasurementsModal>
      <AddMeasurementsModal
        visible={addMeasurementsModalVisible}
        onClose={() => setAddMeasurementsModalVisible(false)}
        onWeightSubmit={handleAddWeight}
        onMeasurementSubmit={handleAddMeasurement}
      ></AddMeasurementsModal>
    </View>
  );
}

export default MeasurementsScreen