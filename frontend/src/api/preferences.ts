import client from './client'
import type { Preference } from '../types/api'

export const getPreferences = () =>
  client.get<Preference[]>('/preferences/')

export const createPreference = (category: string, subcategory?: string) =>
  client.post<Preference>('/preferences/', { category, subcategory })

export const deletePreference = (id: number) =>
  client.delete(`/preferences/${id}`)