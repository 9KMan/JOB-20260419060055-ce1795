import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authService = {
  register: async (email: string, password: string, fullName?: string) => {
    const response = await api.post('/auth/register', {
      email,
      password,
      full_name: fullName,
    })
    return response.data
  },

  login: async (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  getMe: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

export const aiService = {
  generate: async (
    prompt: string,
    systemPrompt?: string,
    maxTokens?: number,
    temperature?: number
  ) => {
    const response = await api.post('/ai/generate', {
      prompt,
      system_prompt: systemPrompt,
      max_tokens: maxTokens,
      temperature: temperature,
    })
    return response.data
  },

  chat: async (messages: Array<{ role: string; content: string }>) => {
    const response = await api.post('/ai/chat', { messages })
    return response.data
  },
}

export const dataService = {
  listItems: async (table: string = 'items') => {
    const response = await api.get(`/data/items?table=${table}`)
    return response.data
  },

  createItem: async (table: string, data: Record<string, unknown>) => {
    const response = await api.post(`/data/items?table=${table}`, data)
    return response.data
  },
}

export default api
