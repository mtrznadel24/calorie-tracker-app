import { View, Text } from 'react-native'
import React, { useState } from 'react'
import SearchBar from '@/components/SearchBar';

const FridgeMealsScreen = () => {
  const [searchText, setSearchText] = useState('');

  return (
    <View>
      <View>
        <SearchBar value={searchText} onChangeText={setSearchText} placeholder="Search meals" />
      </View>
      <Text>Meals</Text>
    </View>
  )
}

export default FridgeMealsScreen