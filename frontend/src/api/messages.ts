import client from './client'
import type { Message } from '../types/api'

export const getConversation = (userId: number) =>
  client.get<Message[]>(`/messages/${userId}`)