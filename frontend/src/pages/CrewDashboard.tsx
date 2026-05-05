import { useEffect, useState } from "react";
import api from "../api";
import type { ComplianceStats } from "../types";

export default function CrewDashboard() {
  const [stats, setStats] = useState<ComplianceStats | null>(null);

  useEffect(() => {
    api.get<ComplianceStats>("/compliance").then((r) => setStats(r.data));
  }, []);

  if (!stats) return <div className="p-8 text-gray-400">Loading...</div>;

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Crew Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Maintenance Compliance</p>
          <p className="text-3xl font-bold text-blue-600">{stats.maintenance_pct}%</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Drill Participation</p>
          <p className="text-3xl font-bold text-green-600">{stats.drill_pct}%</p>
        </div>
        <div className="bg-white rounded-lg shadow p-4">
          <p className="text-sm text-gray-500">Overdue Tasks</p>
          <p className={`text-3xl font-bold ${stats.overdue_tasks > 0 ? "text-red-600" : "text-green-600"}`}>{stats.overdue_tasks}</p>
        </div>
      </div>
    </div>
  );
}
