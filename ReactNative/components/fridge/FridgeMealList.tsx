import { View, Text, StyleSheet } from 'react-native'
import React from 'react'
import {Meal} from "@/services/fridgeMealsService";

interface FridgeMealListProps {
  onMealPress: (meal: Meal) => void
}

const FridgeMealList = ({onMealPress}: FridgeMealListProps) => {


  return (
    <View>
      <Text>FridgeMealList</Text>
    </View>
  )
}

export default FridgeMealList