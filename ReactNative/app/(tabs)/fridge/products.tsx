import { View, Text, Pressable } from 'react-native'
import React, { useState } from 'react'
import SearchBar from '@/components/SearchBar';
import { Ionicons } from "@expo/vector-icons";

const FridgeProductsScreen = () => {
  const [searchText, setSearchText] = useState('');
  const [showFavourites, setShowFavourites] = useState(false);
  const [selectedCategory, setSelectredCategory] = useState<string | null>(null);

  return (
    <View>
      <View className="flex-row items-center gap-3 px-3 py-3">

        <View className="flex-[2] h-12" >
          <SearchBar 
            value={searchText}
            onChangeText={setSearchText}
            placeholder="Search products"
          />
        </View>


        <Pressable
          onPress={() => console.log('open filters')}
          className="flex-[1] h-11 rounded-full items-center justify-center bg-light-200 dark:bg-dark-600"
        >
          <Ionicons name="filter" size={20} />
        </Pressable>
        
        
      </View>
    <Text>Products</Text>
    </View>
  )
}

export default FridgeProductsScreen