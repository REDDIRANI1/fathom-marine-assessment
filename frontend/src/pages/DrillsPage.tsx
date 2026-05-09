import { useEffect, useState } from "react";
import { useAuth } from "../AuthContext";
import api from "../api";
import { getApiErrorMessage } from "../apiError";
import type { SafetyDrill, Ship, User } from "../types";

export default function DrillsPage() {
  const { user } = useAuth();
  const [drills, setDrills] = useState<SafetyDrill[]>([]);
  const [ships, setShips] = useState<Ship[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [selectedDrill, setSelectedDrill] = useState<string | null>(null);
  const [attendanceUsers, setAttendanceUsers] = useState<User[]>([]);
  const [attendanceMap, setAttendanceMap] = useState<Record<string, boolean>>({});
  const [attendanceRecords, setAttendanceRecords] = useState<Record<string, boolean>>({});
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    drill_type: "",
    scheduled_date: "",
    ship_id: "",
    description: "",
  });

  useEffect(() => {
    void loadDrills();
    if (user?.role === "admin") api.get<Ship[]>("/ships").then((r) => setShips(r.data)).catch(() => {});
  }, [user]);

  async function loadDrills() {
    try {
      const res = await api.get<SafetyDrill[]>("/drills");
      setDrills(res.data);
      setError("");
    } catch (err) {
      setError(getApiErrorMessage(err, "Unable to load drills"));
    }
  }

  async function handleCreate() {
    setError("");
    try {
      await api.post("/drills", form);
      setShowForm(false);
      setForm({ drill_type: "", scheduled_date: "", ship_id: "", description: "" });
      await loadDrills();
    } catch (err) {
      setError(getApiErrorMessage(err, "Unable to schedule drill"));
    }
  }

  async function markComplete(id: string) {
    setError("");
    try {
      await api.patch(`/drills/${id}/complete`);
      await loadDrills();
    } catch (err) {
      setError(getApiErrorMessage(err, "Unable to mark drill complete"));
    }
  }

  async function openAttendance(drillId: string) {
    setSelectedDrill(drillId);
    setAttendanceMap({});
    setError("");
    try {
      const [usersRes, recordsRes] = await Promise.all([
        api.get<User[]>("/auth/users"),
        api.get<{ user_id: string; attended: boolean }[]>(`/drills/${drillId}/attendance`),
      ]);
      setAttendanceUsers(usersRes.data);
      const recMap: Record<string, boolean> = {};
      recordsRes.data.forEach((r) => { recMap[r.user_id] = r.attended; });
      setAttendanceRecords(recMap);
    } catch (err) {
      setAttendanceUsers([]);
      setAttendanceRecords({});
      setError(getApiErrorMessage(err, "Unable to load attendance details"));
    }
  }

  async function submitAttendance() {
    if (!selectedDrill) return;
    const entries = Object.entries(attendanceMap).map(([user_id, attended]) => ({ user_id, attended }));
    if (entries.length === 0) return;
    setError("");
    try {
      await api.post(`/drills/${selectedDrill}/attendance`, entries);
      setSelectedDrill(null);
      await loadDrills();
    } catch (err) {
      setError(getApiErrorMessage(err, "Unable to save attendance"));
    }
  }

  function getShipLabel(drill: SafetyDrill) {
    return drill.ship_name || drill.ship_id;
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

      {error && <p className="rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p>}

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

      {selectedDrill && (
        <div className="bg-white rounded-lg shadow p-4 space-y-3">
          <h2 className="font-semibold">Mark Attendance</h2>
          {attendanceUsers.length === 0 && <p className="text-gray-400 text-sm">No crew members available for this ship.</p>}
          {attendanceUsers.map((u) => (
            <label key={u.id} className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={attendanceMap[u.id] ?? attendanceRecords[u.id] ?? false}
                onChange={(e) => setAttendanceMap({ ...attendanceMap, [u.id]: e.target.checked })}
              />
              <span>{u.name} ({u.email})</span>
            </label>
          ))}
          <div className="flex gap-2">
            <button onClick={submitAttendance} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Save Attendance</button>
            <button onClick={() => setSelectedDrill(null)} className="text-gray-500 px-4 py-2 rounded hover:bg-gray-100">Cancel</button>
          </div>
        </div>
      )}

      <div className="space-y-3">
        {drills.map((drill) => (
          <div key={drill.id} className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
            <div>
              <h3 className="font-semibold text-lg capitalize">{drill.drill_type.replace("_", " ")} Drill</h3>
              <p className="text-sm text-gray-500">Scheduled: {drill.scheduled_date} · Ship: {getShipLabel(drill)}</p>
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
                <>
                  <button onClick={() => openAttendance(drill.id)} className="bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700">
                    Attendance
                  </button>
                  <button onClick={() => markComplete(drill.id)} className="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700">
                    Mark Complete
                  </button>
                </>
              )}
            </div>
          </div>
        ))}
        {drills.length === 0 && <p className="text-gray-400 text-center py-8">No drills scheduled</p>}
      </div>
    </div>
  );
}
