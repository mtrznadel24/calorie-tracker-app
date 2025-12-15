import { Colors } from '@/constants/theme';
import { Ionicons } from '@expo/vector-icons';
import React from 'react';
import { TextInput, useColorScheme, View } from 'react-native';

type SearchBarProps = {
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
};

const SearchBar: React.FC<SearchBarProps> = ({ value, onChangeText, placeholder = "Search"}) => {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  return (
    <View
      className="flex-row items-center rounded-full px-4"
      style={{
        backgroundColor: isDark ? Colors.dark[600] : Colors.light[200],
      }}
    >
      <Ionicons
        name="search"
        size={20}
        color={isDark ? Colors.light[100] : Colors.dark[700]}
      />
      <TextInput
        underlineColorAndroid="transparent"
        className="ml-3 flex-1 text-base"
        style={{
          color: isDark ? Colors.light[100] : Colors.dark[700]
        }}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={isDark ? Colors.light[300] : Colors.dark[700]}
      />
    </View>
  );
};

export default SearchBar;