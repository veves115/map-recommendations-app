import apiClient from './client'
import type { Invite, InvitePreview, Friend, Friendship } from '@/types/api'

// ----- Invites -----

export const createInvite = () => {
  return apiClient.post<Invite>('api/v1/friends/invites')
}

export const listInvites = () => {
  return apiClient.get<Invite[]>('api/v1/friends/invites')
}

export const deleteInvite = (id: number) => {
  return apiClient.delete(`api/v1/friends/invites/${id}`)
}

export const lookupInviteByCode = (code: string) => {
  return apiClient.get<InvitePreview>(`api/v1/friends/invites/lookup/${code}`)
}

export const acceptInviteByToken = (token: string) => {
  return apiClient.post<Friendship>(`api/v1/friends/invites/${token}/accept`)
}

export const acceptInviteByCode = (code: string) => {
  return apiClient.post<Friendship>(`api/v1/friends/invites/code/${code}/accept`)
}

// ----- Friends -----

export const listFriends = () => {
  return apiClient.get<Friend[]>('api/v1/friends/')
}

export const removeFriend = (userId: number) => {
  return apiClient.delete(`api/v1/friends/${userId}`)
}

