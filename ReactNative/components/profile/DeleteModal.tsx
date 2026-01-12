import { View, Text, Modal, TextInput, Pressable, KeyboardAvoidingView, Platform, TouchableWithoutFeedback, Keyboard, ActivityIndicator } from 'react-native'
import React, { useState, useEffect } from 'react'
import { Ionicons } from "@expo/vector-icons";

interface DeleteModalProps {
  visible: boolean,
  onClose: () => void,
  onSave: (password: string) => Promise<void>,
}

const DeleteModal = ({ visible, onClose, onSave }: DeleteModalProps) => {
  const [password, setPassword] = useState('')
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (visible) {
      setPassword('');
      setIsSaving(false);
    }
  }, [visible]);

  const handleSave = async () => {
    if (!password || isSaving) return;
    setIsSaving(true);
    await onSave(password);
    setIsSaving(false);
  }

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={() => { Keyboard.dismiss(); onClose(); }}>
        <View className="flex-1 bg-black/60 justify-center px-6">
          <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} className="bg-light-100 dark:bg-dark-800 rounded-3xl p-6 shadow-2xl border border-red-200 dark:border-red-900/50">

              <View className="flex-row justify-between items-center mb-4">
                <Text className="text-xl font-bold text-red-600 dark:text-red-500">Delete Account</Text>
                <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-700 rounded-full">
                  <Ionicons name="close" size={20} color="#9CA3AF" />
                </Pressable>
              </View>

              <View className="bg-red-50 dark:bg-red-900/20 p-4 rounded-xl mb-6">
                 <Text className="text-red-800 dark:text-red-300 text-sm leading-5">
                    This action is irreversible. All your data including measurements, goals, and history will be permanently deleted.
                 </Text>
              </View>

              <Text className="text-gray-500 text-xs mb-2 ml-1 uppercase font-bold">Confirm with Password</Text>
              <TextInput
                value={password}
                onChangeText={setPassword}
                placeholder="Enter your password"
                placeholderTextColor="#9CA3AF"
                secureTextEntry
                className="bg-light-50 dark:bg-dark-900 border border-light-300 dark:border-dark-600 rounded-xl p-4 text-dark-900 dark:text-white text-base mb-6"
              />

              <View className="gap-3">
                <Pressable
                  onPress={handleSave}
                  disabled={isSaving}
                  className="w-full py-4 rounded-2xl items-center justify-center bg-red-500 active:opacity-90"
                >
                  {isSaving ? <ActivityIndicator color="white" /> : <Text className="text-lg font-bold text-white">Delete Permanently</Text>}
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

export default DeleteModal