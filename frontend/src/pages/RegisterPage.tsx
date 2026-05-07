import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { useAuth } from "../AuthContext";
import api from "../api";
import type { Ship } from "../types";

export default function RegisterPage() {
  const { register, loading } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"admin" | "crew">("crew");
  const [shipId, setShipId] = useState("");
  const [ships, setShips] = useState<Ship[]>([]);
  const [error, setError] = useState("");

  async function loadShips() {
    try {
      const res = await api.get<Ship[]>("/ships/names");
      setShips(res.data);
    } catch {
      // ignore on failure
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    if (role === "crew" && !shipId) {
      setError("Please select a ship");
      return;
    }

    try {
      await register({ email, password, name, role, ship_id: role === "crew" ? shipId : undefined });
      navigate("/");
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(typeof err.response?.data?.detail === "string" ? err.response.data.detail : "Registration failed");
        return;
      }
      setError("Unable to create your account right now");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm space-y-4">
        <h1 className="text-2xl font-bold text-center">Create Account</h1>
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <input type="text" placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} className="w-full border rounded px-3 py-2" required />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="w-full border rounded px-3 py-2" required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full border rounded px-3 py-2" required />
        <select
          value={role}
          onChange={(e) => {
            const nextRole = e.target.value as "admin" | "crew";
            setRole(nextRole);
            setShipId("");
            if (nextRole === "crew" && ships.length === 0) {
              void loadShips();
            }
          }}
          className="w-full border rounded px-3 py-2"
        >
          <option value="crew">Crew Member</option>
          <option value="admin">Administrator</option>
        </select>
        {role === "crew" && (
          <div>
            <select
              value={shipId}
              onFocus={loadShips}
              onChange={(e) => setShipId(e.target.value)}
              className="w-full border rounded px-3 py-2"
              required
            >
              <option value="">Select Ship</option>
              {ships.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          </div>
        )}
        <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white rounded py-2 font-medium hover:bg-blue-700 disabled:opacity-50">
          {loading ? "Creating..." : "Register"}
        </button>
        <p className="text-sm text-center text-gray-500">
          Already have an account? <Link to="/login" className="text-blue-600 hover:underline">Sign In</Link>
        </p>
      </form>
    </div>
  );
}
