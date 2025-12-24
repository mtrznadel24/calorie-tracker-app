import React from 'react'
import {Stack} from "expo-router";

const Layout = () => {
  return (
    <Stack>
      <Stack.Screen
        name="setup-profile"
        options={{ headerShown: false, title: "setup-profile" }}
      />
      <Stack.Screen
        name="setup-weight"
        options={{ headerShown: false, title: "setup-weight" }}
      />
      <Stack.Screen
        name="setup-activity-level"
        options={{ headerShown: false, title: "setup-activity-level" }}
      />
    </Stack>
  )
}

export default Layout