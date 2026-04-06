export interface User {
    id: number
    email: string
    username: string
    is_active: boolean
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
