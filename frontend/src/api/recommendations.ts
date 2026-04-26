import apiClient from './client'
import type { NearbyPlace } from '@/types/api'

export const getRecommendations = (params: {
  latitude: number
  longitude: number
  radius?: number
  limit?: number
}) => {
  return apiClient.get<NearbyPlace[]>('api/v1/recommendations/', { params })
}
