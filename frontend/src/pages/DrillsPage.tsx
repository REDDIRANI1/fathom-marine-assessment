import { useEffect, useState } from "react";
import { useAuth } from "../AuthContext";
import api from "../api";
import type { SafetyDrill, Ship } from "../types";

export default function DrillsPage() {
  const { user } = useAuth();
  const [drills, setDrills] = useState<SafetyDrill[]>([]);
  const [ships, setShips] = useState<Ship[]>([]);
  const [showForm, setShowForm] = useState(false);

  const [form, setForm] = useState({
    drill_type: "",
    scheduled_date: "",
    ship_id: "",
    description: "",
  });

  useEffect(() => {
    loadDrills();
    if (user?.role === "admin") api.get<Ship[]>("/ships").then((r) => setShips(r.data));
  }, [user]);

  async function loadDrills() {
    const res = await api.get<SafetyDrill[]>("/drills");
    setDrills(res.data);
  }

  async function handleCreate() {
    await api.post("/drills", form);
    setShowForm(false);
    setForm({ drill_type: "", scheduled_date: "", ship_id: "", description: "" });
    loadDrills();
  }

  async function markComplete(id: string) {
    await api.patch(`/drills/${id}/complete`);
    loadDrills();
  }

  return (
    <div className="p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Safety Drills</h1>
        {user?.role === "admin" && (
          <button onClick={() => setShowForm(!showForm)} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            + Schedule Drill
          </button>
        )}
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow p-4 space-y-3">
          <select value={form.drill_type} onChange={(e) => setForm({ ...form, drill_type: e.target.value })} className="w-full border rounded px-3 py-2">
            <option value="">Select Type</option>
            <option value="fire">Fire Drill</option>
            <option value="evacuation">Evacuation Drill</option>
            <option value="man_overboard">Man Overboard</option>
            <option value="abandon_ship">Abandon Ship</option>
            <option value="collision">Collision Response</option>
          </select>
          <input type="date" value={form.scheduled_date} onChange={(e) => setForm({ ...form, scheduled_date: e.target.value })} className="w-full border rounded px-3 py-2" />
          <select value={form.ship_id} onChange={(e) => setForm({ ...form, ship_id: e.target.value })} className="w-full border rounded px-3 py-2">
            <option value="">Select Ship</option>
            {ships.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
          <button onClick={handleCreate} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Schedule</button>
        </div>
      )}

      <div className="space-y-3">
        {drills.map((drill) => (
          <div key={drill.id} className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
            <div>
              <h3 className="font-semibold text-lg capitalize">{drill.drill_type.replace("_", " ")} Drill</h3>
              <p className="text-sm text-gray-500">Scheduled: {drill.scheduled_date} · Ship: {drill.ship_name || drill.ship_id}</p>
            </div>
            <div className="flex items-center gap-3">
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                drill.status === "completed" ? "bg-green-100 text-green-700" :
                drill.status === "missed" ? "bg-red-100 text-red-700" :
                "bg-blue-100 text-blue-700"
              }`}>
                {drill.status}
              </span>
              {drill.status === "scheduled" && (
                <button onClick={() => markComplete(drill.id)} className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
                  Mark Complete
                </button>
              )}
            </div>
          </div>
        ))}
        {drills.length === 0 && <p className="text-gray-400 text-center py-8">No drills scheduled</p>}
      </div>
    </div>
  );
}
