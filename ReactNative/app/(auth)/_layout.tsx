import { View, Text, StyleSheet } from 'react-native'
import React from 'react'
import {Stack} from "expo-router";

const Layout = () => {
  return (
    <Stack>
      <Stack.Screen
        name="login"
        options={{ headerShown: false, title: "Logowanie" }}
      />
      <Stack.Screen
        name="register"
        options={{ headerTitle: "Register", headerBackTitle: "Back" }}
      />
    </Stack>
  )
}

export default Layout