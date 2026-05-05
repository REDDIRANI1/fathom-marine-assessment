import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";

export default function LoginPage() {
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/");
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm space-y-4">
        <h1 className="text-2xl font-bold text-center">Fathom Marine</h1>
        <p className="text-sm text-gray-500 text-center">Sign in to your account</p>
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border rounded px-3 py-2"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border rounded px-3 py-2"
          required
        />
        <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white rounded py-2 font-medium hover:bg-blue-700 disabled:opacity-50">
          {loading ? "Signing in..." : "Sign In"}
        </button>
        <p className="text-sm text-center text-gray-500">
          No account? <a href="/register" className="text-blue-600 hover:underline">Register</a>
        </p>
      </form>
    </div>
  );
}
