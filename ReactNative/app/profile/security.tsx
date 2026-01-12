import { View, Text, ScrollView, Pressable } from 'react-native';
import React, {useState} from 'react';
import { useAuth } from "@/contexts/AuthContext";
import userService from "@/services/userService";
import Toast from "react-native-toast-message";
import MenuButton from "@/components/profile/MenuButton";
import {Ionicons} from "@expo/vector-icons";
import UpdateUsernameModal from "@/components/profile/UpdateUsernameModal";
import UpdateEmailModal from "@/components/profile/UpdateEmailModal";
import UpdatePasswordModal from "@/components/profile/UpdatePasswordModal";
import DeleteModal from "@/components/profile/DeleteModal";

const Security = () => {
  const { user, setUser, logout} = useAuth();
  const [isDeleteModalVisible, setIsDeleteModalVisible] = useState(false);
  const [isUsernameModalVisible, setIsUsernameModalVisible] = useState(false);
  const [isEmailModalVisible, setIsEmailModalVisible] = useState(false);
  const [isPasswordModalVisible, setIsPasswordModalVisible] = useState(false);


  const initial = user?.username ? user.username.charAt(0).toUpperCase() : "?";

  const handleUpdateUsername = async (newUsername: string) => {
    try {
      const updatedUser = await userService.updateProfile({username: newUsername});
      setUser(updatedUser);
      setIsUsernameModalVisible(false);
      Toast.show({type: "success", text1:"User updated successfully."});
    } catch (error) {
      console.error(error);
      Toast.show({type: "error", text1:"Failed to update username."});
    }
  }

  const handleUpdateEmail = async (newEmail: string, repeatEmail: string) => {
    try {
      const updatedUser = await userService.updateEmail({new_email: newEmail, repeat_email: repeatEmail});
      setUser(updatedUser);
      setIsEmailModalVisible(false);
      Toast.show({type: "success", text1:"Email updated successfully."});
    } catch (error) {
      console.error(error);
      Toast.show({type: "error", text1:"Failed to update email."});
    }
  }

  const handleUpdatePassword = async (oldPassword: string, newPassword: string, repeatPassword: string) => {
    try {
      await userService.updatePassword({old_password: oldPassword, new_password: newPassword, repeat_password: repeatPassword});
      setIsPasswordModalVisible(false);
      Toast.show({type: "success", text1:"Password updated successfully."});
    } catch (error) {
      console.error(error);
      Toast.show({type: "error", text1:"Failed to update password."});
    }
  }

  const handleDeleteAccount = async (password: string) => {
    try {
      await userService.deleteUser({password: password});
      setIsDeleteModalVisible(false);
      await logout()
      Toast.show({type: "success", text1:"Account deleted successfully."});
    } catch (error) {
      console.error(error);
      Toast.show({type: "error", text1:"Failed to delete account."});
    }
  }

  return (
    <View className="flex-1 bg-light-100 dark:bg-dark-900">
      <ScrollView contentContainerStyle={{ padding: 24 }}>

        <View className="items-center mt-4 mb-10">
          <View className="w-24 h-24 rounded-full bg-primary/10 dark:bg-primary/20 items-center justify-center mb-4 border-2 border-primary/20">
            <Text className="text-4xl font-bold text-primary">
              {initial}
            </Text>
          </View>

          <Text className="text-2xl font-bold text-dark-900 dark:text-white mb-1">
            {user?.username || "User"}
          </Text>
          <Text className="text-gray-500 dark:text-gray-400">
            {user?.email || "email@example.com"}
          </Text>

          <View className="flex-row items-center mt-2 bg-green-100 dark:bg-green-900/30 px-3 py-1 rounded-full">
             <View className="w-2 h-2 rounded-full bg-green-500 mr-2" />
             <Text className="text-green-700 dark:text-green-400 text-xs font-bold uppercase">
               Account Active
             </Text>
          </View>
        </View>

        <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-4 ml-1">
          Profile Details
        </Text>

        <View className="mb-8">
          <MenuButton
            title="Update Username"
            icon="person-circle-outline"
            onPress={() => setIsUsernameModalVisible(true)}
            color="#3b82f6"
          />
          <MenuButton
            title="Update Email"
            icon="mail-outline"
            onPress={() => setIsEmailModalVisible(true)}
            color="#3b82f6"
          />
        </View>

        <Text className="text-gray-500 dark:text-gray-400 font-bold uppercase text-xs mb-4 ml-1">
          Security
        </Text>

        <View className="mb-8">
          <MenuButton
            title="Change Password"
            icon="lock-closed-outline"
            onPress={() => setIsPasswordModalVisible(true)}
            color="#8b5cf6"
          />
        </View>

        <Pressable
            onPress={() => setIsDeleteModalVisible(true)}
            className="flex-row items-center justify-center p-6 rounded-2xl border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-900/10 active:opacity-70 mt-4"
        >
            <Ionicons name="log-out-outline" size={20} color="#ef4444" />
            <Text className="text-red-500 font-bold ml-2">Delete Account</Text>
        </Pressable>

        <Text className="text-center text-gray-300 dark:text-gray-600 text-xs mt-8">
            App Version 1.0.0
        </Text>

      </ScrollView>
      <UpdateUsernameModal
        visible={isUsernameModalVisible}
        currentUsername={user.username}
        onClose={() => setIsUsernameModalVisible(false)}
        onSave={handleUpdateUsername}
      ></UpdateUsernameModal>
      <UpdateEmailModal
        visible={isEmailModalVisible}
        currentEmail={user.email}
        onClose={() => setIsEmailModalVisible(false)}
        onSave={handleUpdateEmail}
      ></UpdateEmailModal>
      <UpdatePasswordModal
        visible={isPasswordModalVisible}
        onClose={() => setIsPasswordModalVisible(false)}
        onSave={handleUpdatePassword}
      ></UpdatePasswordModal>
      <DeleteModal
        visible={isDeleteModalVisible}
        onClose={() => setIsDeleteModalVisible(false)}
        onSave={handleDeleteAccount}
      ></DeleteModal>
    </View>
  )
}

export default Security