import React from 'react'
import {Stack} from "expo-router";

const Layout = () => {
  return (
    <Stack>
      <Stack.Screen
        name="setup-profile"
        options={{ headerShown: false, title: "setup-profile" }}
      />
    </Stack>
  )
}

export default Layout