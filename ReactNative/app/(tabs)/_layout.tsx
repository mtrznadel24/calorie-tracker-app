import React from 'react';
import { Tabs } from 'expo-router';
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { useColorScheme } from "react-native";
import { colors } from "../constants/colors";

const Layout = () => {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: colorScheme === "dark" ? colors.tabBar.dark.active : colors.tabBar.light.active,
        tabBarInactiveTintColor: colorScheme === "dark" ? colors.tabBar.dark.inactive : colors.tabBar.light.inactive,
        tabBarStyle: {
          height: 62,
          paddingTop: 5,
          backgroundColor: colorScheme === "dark" ? colors.tabBar.dark.background : colors.tabBar.light.background,
          borderTopWidth: 0,
          elevation: 0,
        },
      }}
    >
      <Tabs.Screen
        name="meals"
        options={{
          title: "Meals",
          tabBarIcon: ({ focused, color, size }) => (
            <Ionicons
              name="restaurant"
              size={focused ? size + 2 : size}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="fridge"
        options={{
          title: "Fridge",
          tabBarIcon: ({ focused, color, size }) => (
            <MaterialCommunityIcons
              name="fridge"
              size={focused ? size + 2 : size}
              color={color}
            />
          ),
        }}
      />

      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ focused, color, size }) => (
            <Ionicons
              name="person"
              size={focused ? size + 2 : size}
              color={color}
            />
          ),
        }}
      />
    </Tabs>
  );
}

export default Layout;
