import { View, Text, Modal, TextInput, Pressable, KeyboardAvoidingView, Platform, TouchableWithoutFeedback, Keyboard, ActivityIndicator } from 'react-native'
import React, { useState, useEffect } from 'react'
import { Ionicons } from "@expo/vector-icons";

interface UpdatePasswordProps {
  visible: boolean,
  onClose: () => void,
  onSave: (oldPassword: string, newPassword: string, repeatPassword: string) => Promise<void>,
}

const UpdatePasswordModal = ({ visible, onClose, onSave }: UpdatePasswordProps) => {
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [repeatPassword, setRepeatPassword] = useState('')
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (visible) {
      setOldPassword('');
      setNewPassword('');
      setRepeatPassword('');
      setIsSaving(false);
    }
  }, [visible]);

  const handleSave = async () => {
    if (!oldPassword || !newPassword || !repeatPassword || isSaving) return;
    setIsSaving(true);
    await onSave(oldPassword, newPassword, repeatPassword);
    setIsSaving(false);
  }

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={() => { Keyboard.dismiss(); onClose(); }}>
        <View className="flex-1 bg-black/60 justify-center px-6">
          <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} className="bg-light-100 dark:bg-dark-800 rounded-3xl p-6 shadow-2xl border border-light-200 dark:border-dark-700">

              <View className="flex-row justify-between items-center mb-6">
                <Text className="text-xl font-bold text-dark-900 dark:text-white">Change Password</Text>
                <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-700 rounded-full">
                  <Ionicons name="close" size={20} color="#9CA3AF" />
                </Pressable>
              </View>

              <View className="gap-y-4 mb-6">
                <TextInput
                    value={oldPassword}
                    onChangeText={setOldPassword}
                    placeholder="Current Password"
                    placeholderTextColor="#9CA3AF"
                    secureTextEntry
                    className="bg-light-50 dark:bg-dark-900 border border-light-300 dark:border-dark-600 rounded-xl p-4 text-dark-900 dark:text-white text-base"
                />
                <TextInput
                    value={newPassword}
                    onChangeText={setNewPassword}
                    placeholder="New Password"
                    placeholderTextColor="#9CA3AF"
                    secureTextEntry
                    className="bg-light-50 dark:bg-dark-900 border border-light-300 dark:border-dark-600 rounded-xl p-4 text-dark-900 dark:text-white text-base"
                />
                <TextInput
                    value={repeatPassword}
                    onChangeText={setRepeatPassword}
                    placeholder="Confirm New Password"
                    placeholderTextColor="#9CA3AF"
                    secureTextEntry
                    className="bg-light-50 dark:bg-dark-900 border border-light-300 dark:border-dark-600 rounded-xl p-4 text-dark-900 dark:text-white text-base"
                />
              </View>

              <View className="gap-4">
                <Pressable
                  onPress={handleSave}
                  disabled={isSaving}
                  className="w-full py-4 rounded-2xl items-center justify-center bg-primary active:opacity-90"
                >
                  {isSaving ? <ActivityIndicator color="white" /> : <Text className="text-lg font-bold text-white">Save Changes</Text>}
                </Pressable>

                <Pressable onPress={onClose} disabled={isSaving} className="items-center py-2">
                   <Text className="text-gray-500 font-semibold">Cancel</Text>
                </Pressable>
              </View>
            </KeyboardAvoidingView>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  )
}

export default UpdatePasswordModal