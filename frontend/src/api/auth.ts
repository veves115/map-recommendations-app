import apiClient from './client'

//Endpoints de autenticación
export const register = (email: string, username: string, password: string) => {
  return apiClient.post('api/v1/auth/register', {
    email,
    username,
    password,
  })
}

export const login = (email: string, password: string) => {
  return apiClient.post('api/v1/auth/login', {
    email,
    password,
  })
}

export const getMe = () => {
  return apiClient.get('api/v1/auth/me')
}

export const changePassword = (currentPassword: string, newPassword: string) => {
  return apiClient.post('api/v1/auth/change-password', {
    current_password: currentPassword,
    new_password: newPassword,
  })
}
