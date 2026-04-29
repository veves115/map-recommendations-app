import apiClient from './client'
import type { NearbyPlace, PlaceDetails, GeocodeResult } from '@/types/api'

export const getNearbyPlaces = (params: {
  latitude: number
  longitude: number
  radius?: number
  place_type?: string
  keyword?: string
}) => {
  return apiClient.get<NearbyPlace[]>('api/v1/maps/nearby', { params })
}

export const getPlaceDetails = (placeId: string) => {
  return apiClient.get<PlaceDetails>(`api/v1/maps/place/${placeId}`)
}

export const geocodeAddress = (address: string) => {
  return apiClient.get<GeocodeResult>('api/v1/maps/geocode', {
    params: { address }
  })
}
