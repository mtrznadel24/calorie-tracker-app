import { View, Text, ScrollView } from 'react-native';
import React, { useState } from 'react';
import MenuButton from "@/components/profile/MenuButton";
import { useAuth } from "@/contexts/AuthContext";
import { Ionicons } from "@expo/vector-icons";
import WeightModal from "@/components/profile/WeightModal";
import RateModal from "@/components/profile/RateModal";
import ActivityModal from "@/components/profile/ActivityModal";
import userService from "@/services/userService";
import weightService from "@/services/weightService";
import Toast from "react-native-toast-message";

const StatCard = ({ label, value, unit, icon, color }: any) => (
  <View className="bg-white dark:bg-dark-800 p-4 rounded-2xl border border-light-200 dark:border-dark-700 flex-1 items-center justify-center shadow-sm min-w-[100px]">
    <View className={`w-8 h-8 rounded-full items-center justify-center mb-2 opacity-20`} style={{ backgroundColor: color }}>
        <Ionicons name={icon} size={18} color={color} style={{ opacity: 1 }} />
    </View>
    <Text className="text-2xl font-black text-dark-900 dark:text-light-100">
      {value} <Text className="text-xs font-normal text-gray-500">{unit}</Text>
    </Text>
    <Text className="text-[10px] uppercase font-bold text-gray-400 mt-1 text-center">
      {label}
    </Text>
  </View>
);

const Goals = () => {
  const {user, setUser} = useAuth();

  const [weightModalVisible, setWeightModalVisible] = useState(false);
  const [rateModalVisible, setRateModalVisible] = useState(false);
  const [activityModalVisible, setActivityModalVisible] = useState(false);

  const getActivityLabel = (level: number) => {
    if (level <= 1.2) return "Sedentary";
    if (level <= 1.375) return "Light";
    if (level <= 1.55) return "Moderate";
    if (level <= 1.725) return "Active";
    return "Extra Active";
  };

  const handleSaveWeight = async (newWeight: number) => {
    try {
      const response = await weightService.addWeight({weight: newWeight});
      const weightValue = response?.weight || newWeight;
      const updatedUser = {...user, current_weight: weightValue};
      setUser(updatedUser);

      Toast.show({
        type: 'success',
        text1: 'Weight Updated',
        text2: `Your current weight is now ${newWeight} kg`
      });

    } catch (error) {
      console.log(error);
      Toast.show({
        type: 'error',
        text1: 'Error',
        text2: 'Failed to update weight'
      });
    }
  };

  const handleUpdateRate = async (newRate: number) => {
    try {
      const updatedUser = await userService.updateProfile({target_weekly_gain: newRate});
      setUser(updatedUser);
      Toast.show({
        type: 'success',
        text1: 'Target weekly gain Updated',
        text2: `Your new target weekly gain: ${newRate}`
      });
    } catch (error) {
      console.log(error);
      console.log(error);
      Toast.show({
        type: 'error',
        text1: 'Error',
        text2: 'Failed to update target weekly gain'
      });
    }
  }

  const handleUpdateActivityLevel = async (newLevel: number) => {
    try {
      const updatedUser = await userService.updateProfile({activity_level: newLevel});
      setUser(updatedUser);
      Toast.show({
        type: 'success',
        text1: 'Activity Level Updated',
        text2: `Your new activity level: ${newLevel}`
      });
    } catch (error) {
      console.log(error);
      Toast.show({
        type: 'error',
        text1: 'Error',
        text2: 'Failed to update activity level'
      });
    }
  }

  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-900">
      <ScrollView contentContainerStyle={{padding: 24}}>

        <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-4 ml-1">
          Current Status
        </Text>

        <View className="flex-row gap-3 mb-8">
          <StatCard
            label="Weight"
            value={user?.current_weight || "--"}
            unit="kg"
            icon="scale"
            color="#3b82f6"
          />
          <StatCard
            label="Goal/Week"
            value={user?.target_weekly_gain > 0 ? `+${user.target_weekly_gain}` : user?.target_weekly_gain}
            unit="kg"
            icon="trending-up"
            color="#10b981"
          />
        </View>

        <View
          className="bg-white dark:bg-dark-800 p-4 rounded-2xl border border-light-200 dark:border-dark-700 mb-8 flex-row items-center justify-between shadow-sm">
          <View>
            <Text className="text-gray-400 text-xs font-bold uppercase">Activity Level</Text>
            <Text className="text-xl font-bold text-dark-900 dark:text-white mt-1">
              {getActivityLabel(user?.activity_level || 1.2)}
            </Text>
          </View>
          <Ionicons name="walk" size={32} color="#8b5cf6"/>
        </View>

        <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-4 ml-1">
          Edit Goals
        </Text>

        <View className="mb-8">
          <MenuButton
            title="Update Current Weight"
            icon="scale-outline"
            onPress={() => setWeightModalVisible(true)}
            color="#3b82f6"
          />
          <MenuButton
            title="Change Weekly Rate"
            icon="speedometer-outline"
            onPress={() => setRateModalVisible(true)}
            color="#10b981"
          />
          <MenuButton
            title="Set Activity Level"
            icon="walk-outline"
            onPress={() => setActivityModalVisible(true)}
            color="#8b5cf6"
          />
        </View>

        <Text className="text-center text-gray-400 text-xs px-4">
          Your daily calorie limit is calculated based on these values using the Mifflin-St Jeor formula.
        </Text>

      </ScrollView>
      <WeightModal
        visible={weightModalVisible}
        currentWeight={user.current_weight}
        onClose={() => setWeightModalVisible(false)}
        onSave={handleSaveWeight}
      ></WeightModal>
      <RateModal
        visible={rateModalVisible}
        currentRate={user.target_weekly_gain}
        onClose={() => setRateModalVisible(false)}
        onSave={handleUpdateRate}
      ></RateModal>
      <ActivityModal
        visible={activityModalVisible}
        currentLevel={user.activity_level}
        onClose={() => setActivityModalVisible(false)}
        onSave={handleUpdateActivityLevel}
      ></ActivityModal>
    </View>
  );
}

export default Goals;