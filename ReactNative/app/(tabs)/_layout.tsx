import React from "react";
import { Tabs } from "expo-router";
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { useColorScheme } from "react-native";
import { Colors } from "../../constants/theme";

const Layout = () => {
  const colorScheme = useColorScheme();

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor:
          colorScheme === "dark"
            ? Colors.tabBar.dark.active
            : Colors.tabBar.light.active,
        tabBarInactiveTintColor:
          colorScheme === "dark"
            ? Colors.tabBar.dark.inactive
            : Colors.tabBar.light.inactive,
        tabBarStyle: {
          height: 62,
          paddingTop: 5,
          backgroundColor:
            colorScheme === "dark"
              ? Colors.tabBar.dark.background
              : Colors.tabBar.light.background,
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
};

export default Layout;
