import apiClient from './client'
import type { User } from '@/types/api'

export const listUsers = (skip = 0, limit = 100) => {
  return apiClient.get<User[]>('api/v1/users/', { params: { skip, limit } })
}

export const getUserById = (id: number) => {
  return apiClient.get<User>(`api/v1/users/${id}`)
}

export interface UserUpdate {
  username?: string
  email?: string
}

export const updateMe = (data: UserUpdate) => {
  return apiClient.patch<User>('api/v1/users/me', data)
}

export const deleteMe = () => {
  return apiClient.delete('api/v1/users/me')
}

