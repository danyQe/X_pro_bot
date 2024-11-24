export const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000',
  endpoints: {
    sentiment: '/sentiment',
    facts: '/facts',
    viral: '/viral'
  }
}