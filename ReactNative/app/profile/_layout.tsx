import {Stack, useRouter} from "expo-router";
import { useColorScheme } from "@/hooks/use-color-scheme";
import { Colors } from "@/constants/theme";
import { Pressable, View, Text } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ProfileLayout() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';
  const router = useRouter();

  const headerBackgroundColor = isDark ? Colors.dark[900] : Colors.light[100];
  const headerTextColor = isDark ? Colors.light[100] : Colors.dark[900];
  const headerBorderColor = isDark ? Colors.dark[700] : Colors.light[300];

  return (
    <Stack
      screenOptions={{
        headerShown: true,

        header: ({ options, navigation }) => (
          <View style={{ backgroundColor: headerBackgroundColor }}>
            <SafeAreaView edges={['top']}>
              <View className="h-14 flex-row items-center justify-center px-4 border-b"
                    style={{ borderColor: headerBorderColor }}>

                {navigation.canGoBack() && (
                  <Pressable
                    onPress={() => navigation.goBack()}
                    className="absolute left-4 z-10 p-2"
                  >
                    <Ionicons name="arrow-back" size={24} color={headerTextColor} />
                  </Pressable>
                )}

                <Text className="font-bold text-xl text-dark-900 dark:text-light-100">
                  {options.title}
                </Text>

              </View>
            </SafeAreaView>
          </View>
        ),

        contentStyle: { backgroundColor: headerBackgroundColor },
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
        name="measurements-screen"
        options={{ title: "Measurements" }}
      />
      <Stack.Screen
        name="security"
        options={{ title: "Account Settings" }}
      />
    </Stack>
  );
}