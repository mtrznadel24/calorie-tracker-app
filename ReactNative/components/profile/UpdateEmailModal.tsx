import { View, Text, Modal, TextInput, Pressable, KeyboardAvoidingView, Platform, TouchableWithoutFeedback, Keyboard, ActivityIndicator } from 'react-native'
import React, { useState, useEffect } from 'react'
import { Ionicons } from "@expo/vector-icons";

interface UpdateEmailProps {
  visible: boolean,
  currentEmail: string,
  onClose: () => void,
  onSave: (newEmail: string, repeatEmail: string) => Promise<void>,
}

const UpdateEmailModal = ({ visible, currentEmail, onClose, onSave }: UpdateEmailProps) => {
  const [newEmail, setNewEmail] = useState('')
  const [repeatEmail, setRepeatEmail] = useState('')
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (visible) {
      setNewEmail('');
      setRepeatEmail('');
      setIsSaving(false);
    }
  }, [visible]);

  const handleSave = async () => {
    if (!newEmail || !repeatEmail || isSaving) return;
    setIsSaving(true);
    await onSave(newEmail, repeatEmail);
    setIsSaving(false);
  }

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={() => { Keyboard.dismiss(); onClose(); }}>
        <View className="flex-1 bg-black/60 justify-center px-6">
          <TouchableWithoutFeedback onPress={(e) => e.stopPropagation()}>
            <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : "height"} className="bg-light-100 dark:bg-dark-800 rounded-3xl p-6 shadow-2xl border border-light-200 dark:border-dark-700">

              <View className="flex-row justify-between items-center mb-2">
                <Text className="text-xl font-bold text-dark-900 dark:text-white">Update Email</Text>
                <Pressable onPress={onClose} className="p-2 bg-light-200 dark:bg-dark-700 rounded-full">
                  <Ionicons name="close" size={20} color="#9CA3AF" />
                </Pressable>
              </View>

              <Text className="text-gray-400 text-sm mb-6">Current: {currentEmail}</Text>

              <View className="gap-y-4 mb-6">
                <View>
                    <Text className="text-gray-500 text-xs mb-2 ml-1 uppercase font-bold">New Email</Text>
                    <TextInput
                        value={newEmail}
                        onChangeText={setNewEmail}
                        placeholder="new@example.com"
                        placeholderTextColor="#9CA3AF"
                        className="bg-light-50 dark:bg-dark-900 border border-light-300 dark:border-dark-600 rounded-xl p-4 text-dark-900 dark:text-white text-base"
                        keyboardType="email-address"
                        autoCapitalize="none"
                    />
                </View>
                <View>
                    <Text className="text-gray-500 text-xs mb-2 ml-1 uppercase font-bold">Confirm Email</Text>
                    <TextInput
                        value={repeatEmail}
                        onChangeText={setRepeatEmail}
                        placeholder="Repeat new email"
                        placeholderTextColor="#9CA3AF"
                        className="bg-light-50 dark:bg-dark-900 border border-light-300 dark:border-dark-600 rounded-xl p-4 text-dark-900 dark:text-white text-base"
                        keyboardType="email-address"
                        autoCapitalize="none"
                    />
                </View>
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

export default UpdateEmailModal