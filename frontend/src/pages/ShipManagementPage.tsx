import { useEffect, useState } from "react";
import { useAuth } from "../AuthContext";
import api from "../api";
import type { Ship } from "../types";

export default function ShipManagementPage() {
  const { user } = useAuth();
  const [ships, setShips] = useState<Ship[]>([]);
  const [name, setName] = useState("");

  useEffect(() => {
    api.get<Ship[]>("/ships").then((r) => setShips(r.data));
  }, []);

  async function handleCreate() {
    if (!name.trim()) return;
    await api.post("/ships", { name });
    setName("");
    const r = await api.get<Ship[]>("/ships");
    setShips(r.data);
  }

  if (user?.role !== "admin") return null;

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Ships</h1>
      <div className="flex gap-2">
        <input type="text" placeholder="Ship name" value={name} onChange={(e) => setName(e.target.value)} className="border rounded px-3 py-2 flex-1" />
        <button onClick={handleCreate} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Add Ship</button>
      </div>
      <div className="space-y-2">
        {ships.map((ship) => (
          <div key={ship.id} className="bg-white rounded-lg shadow p-3">{ship.name}</div>
        ))}
      </div>
    </div>
  );
}
