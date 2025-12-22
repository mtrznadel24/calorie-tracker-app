import { SafeAreaView } from "react-native-safe-area-context";
import { createMaterialTopTabNavigator } from "@react-navigation/material-top-tabs";
import { useColorScheme } from "react-native";
import { Colors } from "@/constants/theme";

import FridgeMealsScreen from "./meals";
import FridgeProductsScreen from "./products";

const Tab = createMaterialTopTabNavigator();

export default function FridgeLayout() {
  const isDark = useColorScheme() === "dark";

  return (
    <SafeAreaView
      style={{
        flex: 1,
        backgroundColor: isDark ? Colors.dark[800] : Colors.light[100],
      }}
      edges={["top"]}
    >
      <Tab.Navigator
        screenOptions={{
          tabBarIndicatorStyle: {
            backgroundColor: Colors.primary,
          },
          tabBarStyle: {
            backgroundColor: isDark ? Colors.dark[800] : Colors.light[100],
          },
          tabBarLabelStyle: {
            fontWeight: "600",
          },
          tabBarActiveTintColor: Colors.primary,
          tabBarInactiveTintColor: isDark ? "#9CA3AF" : "#6B7280",
        }}
      >
        <Tab.Screen
          name="meals"
          options={{ title: "Meals" }}
          component={FridgeMealsScreen}
        />
        <Tab.Screen
          name="products"
          options={{ title: "Products" }}
          component={FridgeProductsScreen}
        />
      </Tab.Navigator>
    </SafeAreaView>
  );
}
