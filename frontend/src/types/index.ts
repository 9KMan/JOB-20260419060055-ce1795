export interface User {
  id: string
  email: string
  full_name?: string
  created_at: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface AIRequest {
  prompt: string
  system_prompt?: string
  max_tokens?: number
  temperature?: number
}

export interface AIResponse {
  result: string
}
