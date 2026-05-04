export interface User {
    id: number
    email: string
    username: string
    is_active: boolean
    share_location: boolean
    created_at: string
}

export interface Preference {
    id: number
    user_id: number
    category: string
    subcategory?: string
    created_at: string
}

export interface Location {
    id: number
    user_id: number
    latitude: number
    longitude: number
    timestamp: string
}

export interface Message {
    id: number
    sender_id: number
    receiver_id: number
    content: string
    is_read: boolean
    timestamp: string
}

export interface Token {
    access_token: string
    token_type: string
}

export interface Recommendation {
    place_id: string
    name: string
    rating: number
    vicinity: string
    types: string[]
}

export interface LatLng {
  lat: number
  lng: number
}

export interface NearbyPlace {
  place_id: string
  name: string
  address: string | null
  types: string[]
  rating: number | null
  user_ratings_total: number | null
  location: LatLng
  open_now: boolean | null
  photos: string[]
}

export interface PlaceReview {
  author: string
  rating: number
  text: string
  time: number
}

export interface PlaceDetails {
  place_id: string
  name: string
  formatted_address: string | null
  phone: string | null
  website: string | null
  rating: number | null
  user_ratings_total: number | null
  price_level: number | null
  types: string[]
  location: LatLng
  opening_hours: string[] | null
  reviews: PlaceReview[]
}

export interface GeocodeResult {
  formatted_address: string
  location: LatLng
  place_id: string
}
// ===== Friendships =====

export interface Invite {
  id: number
  token: string
  code: string
  expires_at: string
  used_at: string | null
  created_at: string
}

export interface InvitePreview {
  code: string
  inviter: User
  expires_at: string
  is_valid: boolean
}

export interface Friend {
  user: User
  friendship_id: number
  friends_since: string
}

export interface Friendship {
  id: number
  requester: User
  addressee: User
  status: 'pending' | 'accepted'
  created_at: string
  responded_at: string | null
}



