import apiClient from './client'
import type { Preference } from '@/types/api'

export interface PreferenceCreate {
  category: string
  subcategory?: string | null
}

export const listPreferences = (skip = 0, limit = 20) => {
  return apiClient.get<Preference[]>('api/v1/preferences/', {
    params: { skip, limit },
  })
}

export const createPreference = (data: PreferenceCreate) => {
  return apiClient.post<Preference>('api/v1/preferences/', data)
}

export const deletePreference = (id: number) => {
  return apiClient.delete(`api/v1/preferences/${id}`)
}

export const updatePreference = (id: number, data: PreferenceCreate) => {
  return apiClient.put<Preference>(`api/v1/preferences/${id}`, data)
}
