import { useState } from 'react'
import { useAuth } from '../../src/context/AuthContext'

export default function AuthModal({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { signInWithEmail, signUpWithEmail } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [mode, setMode] = useState<'signin' | 'signup'>('signin')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  if (!open) return null

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    const action = mode === 'signin' ? signInWithEmail : signUpWithEmail
    const { error } = await action(email, password)
    setLoading(false)
    if (error) {
      setError(error)
    } else {
      if (mode === 'signin') onClose()
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-[200]">
      <div className="bg-white rounded-lg w-full max-w-sm p-6 border-2 border-gray-200">
        <h2 className="text-lg font-semibold mb-4">{mode === 'signin' ? 'Sign in' : 'Sign up'}</h2>
        <form onSubmit={onSubmit} className="space-y-3">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            className="w-full border rounded px-3 py-2"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full border rounded px-3 py-2"
            required
          />
          {error && <div className="text-sm text-red-600">{error}</div>}
          <button disabled={loading} className="w-full bg-gray-900 text-white rounded py-2 disabled:opacity-50">
            {loading ? 'Loading...' : (mode === 'signin' ? 'Sign in' : 'Sign up')}
          </button>
        </form>
        <div className="mt-3 text-sm text-gray-700">
          {mode === 'signin' ? (
            <button className="underline" onClick={() => setMode('signup')}>Create an account</button>
          ) : (
            <button className="underline" onClick={() => setMode('signin')}>Have an account? Sign in</button>
          )}
        </div>
        {mode === 'signup' && (
          <p className="text-xs text-gray-600 mt-2">We require email confirmation. Check your inbox after sign up.</p>
        )}
        <button className="absolute top-3 right-3" onClick={onClose}>✕</button>
      </div>
    </div>
  )
}
