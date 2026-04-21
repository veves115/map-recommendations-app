import apiClient from "./client";

//Endpoints de autenticación
export const register = (email: string, username: string, password: string) => {
    return apiClient.post('/auth/register', {
        email,
        username,
        password
    })
}

export const login = (email: string, password: string) => {
    return apiClient.post('/auth/login', {
        email,
        password
    })
}

export const getMe = () => {
    return apiClient.get('/auth/me')
}

