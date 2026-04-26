import apiClient from './client'
import type { Message } from '@/types/api'

export interface MessageCreate {
  receiver_id: number
  content: string
}

export const getConversation = (userId: number, skip = 0, limit = 50) => {
  return apiClient.get<Message[]>(`api/v1/messages/${userId}`, {
    params: { skip, limit },
  })
}

export const sendMessage = (data: MessageCreate) => {
  return apiClient.post<Message>('api/v1/messages/', data)
}

export const markAsRead = (messageId: number) => {
  return apiClient.patch<Message>(`api/v1/messages/${messageId}/read`)
}
