export function useAuth() {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user')

  const isAuthenticated = () => !!token

  const logout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return {
    token,
    user: user ? JSON.parse(user) : null,
    isAuthenticated: isAuthenticated(),
    logout,
  }
}
