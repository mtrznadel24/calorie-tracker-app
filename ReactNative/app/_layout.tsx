import "./globals.css";
import {
  DarkTheme as NavigationDarkTheme,
  DefaultTheme as NavigationDefaultTheme,
  ThemeProvider,
} from "@react-navigation/native";
import {Stack, useRouter, useSegments} from "expo-router";
import { StatusBar } from "expo-status-bar";
import "react-native-reanimated";
import { useColorScheme } from "@/hooks/use-color-scheme";
import { Colors } from "../constants/theme";
import {AuthProvider, useAuth} from "@/contexts/AuthContext";
import {useEffect} from "react";
import {ActivityIndicator, View} from "react-native";
import Toast from "react-native-toast-message";

export const unstable_settings = {
  anchor: "(tabs)",
};

const MyDarkTheme = {
  ...NavigationDarkTheme,
  colors: {
    ...NavigationDarkTheme.colors,
    primary: Colors.primary,
    background: Colors.dark[800],
    card: Colors.dark[700],
    text: Colors.light[100],
    border: Colors.dark[700],
    notification: Colors.accent,
  },
};

const MyLightTheme = {
  ...NavigationDefaultTheme,
  colors: {
    ...NavigationDefaultTheme.colors,
    primary: Colors.primary,
    background: Colors.light[100],
    card: Colors.light[100],
    text: Colors.dark[700],
    border: Colors.light[200],
    notification: Colors.accent,
  },
};

const InitialLayout = () => {
  const { user, isLoading } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  const colorScheme = useColorScheme();
  const isDark = colorScheme === "dark";
  const rootBg = isDark ? Colors.dark[800] : Colors.light[100];

  const backgroundColor = isDark ? Colors.dark[800] : Colors.light[100];

  useEffect(() => {
    if (isLoading) return;

    const inAuthGroup = segments[0] === "(auth)";
    if (!user && !inAuthGroup) {
      router.replace("/(auth)/login");
    } else if (user && inAuthGroup) {
      router.replace("/(tabs)/meals")
    }
  }, [user, isLoading, segments]);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: backgroundColor }}>
        <ActivityIndicator size="large" color={Colors.primary} />
      </View>
    );
  }

  return (
    <View style={{ flex: 1, backgroundColor: rootBg }}>
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: backgroundColor },
          animation: 'slide_from_right',
        }}
      >
        <Stack.Screen name="(tabs)"/>
        <Stack.Screen name="(auth)"/>
        <Stack.Screen name="(onboarding)"/>
        <Stack.Screen name="profile" />
      </Stack>
    </View>
  )
}

export default function RootLayout() {
  const colorScheme = useColorScheme();

  return (
    <ThemeProvider value={colorScheme === "dark" ? MyDarkTheme : MyLightTheme}>
      <AuthProvider>
        <InitialLayout/>
        <StatusBar style={colorScheme === "dark" ? "light" : "dark"} />
        <Toast />
      </AuthProvider>
    </ThemeProvider>
  );
}
