import { useEffect, useState } from "react";
import { useAuth } from "../AuthContext";
import api from "../api";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";
import type { ComplianceStats, ShipCompliance } from "../types";

const COLORS = ["#22c55e", "#ef4444", "#eab308"];

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState<ComplianceStats | null>(null);
  const [ships, setShips] = useState<ShipCompliance[]>([]);

  useEffect(() => {
    api.get<ComplianceStats>("/compliance").then((r) => setStats(r.data));
    if (user?.role === "admin") {
      api.get<ShipCompliance[]>("/compliance/ships").then((r) => setShips(r.data));
    }
  }, [user]);

  if (!stats) return <div className="p-8 text-gray-400">Loading...</div>;

  const pieData = [
    { name: "Compliant", value: stats.overall_pct },
    { name: "At Risk", value: 100 - stats.overall_pct },
  ];

  const barData = ships.map((s) => ({ name: s.ship_name, maintenance: s.maintenance_pct, drills: s.drill_pct }));

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Compliance Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card title="Maintenance" value={`${stats.maintenance_pct}%`} color="text-blue-600" />
        <Card title="Safety Drills" value={`${stats.drill_pct}%`} color="text-green-600" />
        <Card title="Overall" value={`${stats.overall_pct}%`} color={stats.overall_pct >= 80 ? "text-green-600" : "text-red-600"} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-2">Compliance Summary</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" outerRadius={90} dataKey="value">
                <Cell fill={COLORS[0]} />
                <Cell fill={COLORS[2]} />
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-2">Alerts</h2>
          <div className="space-y-2">
            <Alert label="Overdue tasks" count={stats.overdue_tasks} variant="danger" />
            <Alert label="Missed drills" count={stats.missed_drills} variant="warning" />
          </div>
        </div>
      </div>

      {ships.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="font-semibold mb-4">Ship-by-Ship Compliance</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="maintenance" fill="#3b82f6" name="Maintenance %" />
              <Bar dataKey="drills" fill="#22c55e" name="Drills %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

function Card({ title, value, color }: { title: string; value: string; color: string }) {
  return (
    <div className="bg-white rounded-lg shadow p-4">
      <p className="text-sm text-gray-500">{title}</p>
      <p className={`text-3xl font-bold ${color}`}>{value}</p>
    </div>
  );
}

function Alert({ label, count, variant }: { label: string; count: number; variant: "danger" | "warning" }) {
  const bg = variant === "danger" ? "bg-red-50 border-red-200 text-red-700" : "bg-yellow-50 border-yellow-200 text-yellow-700";
  return (
    <div className={`p-3 rounded border ${bg}`}>
      <span className="font-semibold">{label}: </span>
      <span>{count}</span>
    </div>
  );
}
