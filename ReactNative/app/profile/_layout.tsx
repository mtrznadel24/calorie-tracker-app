import { Stack, useRouter } from "expo-router";
import { useColorScheme } from "@/hooks/use-color-scheme";
import { Colors } from "@/constants/theme";
import { Pressable } from "react-native";
import { Ionicons } from "@expo/vector-icons";

export default function ProfileLayout() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';
  const router = useRouter();

  const headerBackgroundColor = isDark ? Colors.dark[900] : Colors.light[100];
  const headerTextColor = isDark ? Colors.light[100] : Colors.dark[900];

  const contentBackgroundColor = isDark ? Colors.dark[900] : Colors.light[100];

  return (
    <Stack
      screenOptions={{
        headerShown: true,
        headerStyle: {
          backgroundColor: headerBackgroundColor,
        },
        headerTintColor: headerTextColor,
        headerTitleStyle: {
          fontWeight: 'bold',
        },
        headerShadowVisible: false,

        contentStyle: { backgroundColor: contentBackgroundColor },

        headerLeft: ({ canGoBack }) =>
          canGoBack ? (
            <Pressable onPress={() => router.back()} className="mr-4">
               <Ionicons name="arrow-back" size={24} color={headerTextColor} />
            </Pressable>
          ) : null,
      }}
    >
      <Stack.Screen
        name="details"
        options={{ title: "Personal Info" }}
      />
      <Stack.Screen
        name="goals"
        options={{ title: "Body & Goals" }}
      />
      <Stack.Screen
        name="measurements"
        options={{ title: "Measurements" }}
      />
      <Stack.Screen
        name="security"
        options={{ title: "Account Settings" }}
      />
    </Stack>
  );
}