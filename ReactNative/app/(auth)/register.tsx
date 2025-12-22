import { View, Text, StyleSheet } from 'react-native'
import React from 'react'
import {z} from "zod";

const registerSchema = z.object({
  username: z.string().min(3, "Useraname need to be at least 3 characters"),
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password need to be at least 8 characters"),
  confirmPassword: z.string(),

})

const Register = () => {
  return (
    <View>
      <Text>Register</Text>
    </View>
  )
}

export default Register