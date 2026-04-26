import apiClient from './client'
import type { User } from '@/types/api'

export const listUsers = (skip = 0, limit = 100) => {
  return apiClient.get<User[]>('api/v1/users/', { params: { skip, limit } })
}

export const getUserById = (id: number) => {
  return apiClient.get<User>(`api/v1/users/${id}`)
}
