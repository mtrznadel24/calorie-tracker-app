import { View, Text } from 'react-native'
import React from 'react'

const Meals = () => {
  return (
      <View className="flex-1 bg-light-100 dark:bg-dark-800 items-center justify-center p-4">
        <Text className="text-2xl font-bold text-dark-700 dark:text-light-100 mb-2">
          Meals Screen
        </Text>
      </View>
    );
}

export default Meals