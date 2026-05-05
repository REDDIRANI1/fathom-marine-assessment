import { useEffect, useState } from "react";
import { useAuth } from "../AuthContext";
import api from "../api";
import type { MaintenanceTask, Ship } from "../types";

export default function MaintenancePage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<MaintenanceTask[]>([]);
  const [ships, setShips] = useState<Ship[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState({ status: "", ship_id: "" });
  const [commentText, setCommentText] = useState<Record<string, string>>({});

  const [form, setForm] = useState({ title: "", due_date: "", ship_id: "", description: "", assigned_to: "" });

  useEffect(() => {
    loadTasks();
    if (user?.role === "admin") api.get<Ship[]>("/ships").then((r) => setShips(r.data));
  }, [user, filter]);

  async function loadTasks() {
    const params: Record<string, string> = {};
    if (filter.status) params.status = filter.status;
    if (filter.ship_id) params.ship_id = filter.ship_id;
    const res = await api.get<MaintenanceTask[]>("/tasks", { params });
    setTasks(res.data);
  }

  async function handleCreate() {
    await api.post("/tasks", form);
    setShowForm(false);
    setForm({ title: "", due_date: "", ship_id: "", description: "", assigned_to: "" });
    loadTasks();
  }

  async function updateStatus(id: string, status: string) {
    await api.patch(`/tasks/${id}/status`, { status });
    loadTasks();
  }

  async function addComment(taskId: string) {
    if (!commentText[taskId]) return;
    await api.post(`/tasks/${taskId}/comments`, { content: commentText[taskId] });
    setCommentText({ ...commentText, [taskId]: "" });
    loadTasks();
  }

  return (
    <div className="p-6 space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Maintenance Tasks</h1>
        {user?.role === "admin" && (
          <button onClick={() => setShowForm(!showForm)} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            + New Task
          </button>
        )}
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow p-4 space-y-3">
          <input type="text" placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="w-full border rounded px-3 py-2" />
          <input type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} className="w-full border rounded px-3 py-2" />
          <select value={form.ship_id} onChange={(e) => setForm({ ...form, ship_id: e.target.value })} className="w-full border rounded px-3 py-2">
            <option value="">Select Ship</option>
            {ships.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
          <textarea placeholder="Description (optional)" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} className="w-full border rounded px-3 py-2" />
          <button onClick={handleCreate} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">Save</button>
        </div>
      )}

      <div className="flex gap-3 flex-wrap">
        <select value={filter.status} onChange={(e) => setFilter({ ...filter, status: e.target.value })} className="border rounded px-3 py-2">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
        {user?.role === "admin" && (
          <select value={filter.ship_id} onChange={(e) => setFilter({ ...filter, ship_id: e.target.value })} className="border rounded px-3 py-2">
            <option value="">All Ships</option>
            {ships.map((s) => <option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        )}
      </div>

      <div className="space-y-3">
        {tasks.map((task) => (
          <div key={task.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="font-semibold text-lg">{task.title}</h3>
                <p className="text-sm text-gray-500">Due: {task.due_date} · Ship: {task.ship_name || task.ship_id}</p>
                <div className="flex gap-2 mt-2">
                  {(["pending", "in_progress", "completed"] as const).map((s) => (
                    <button
                      key={s}
                      onClick={() => updateStatus(task.id, s)}
                      className={`px-3 py-1 rounded text-sm ${task.status === s ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"}`}
                    >
                      {s === "in_progress" ? "In Progress" : s.charAt(0).toUpperCase() + s.slice(1)}
                    </button>
                  ))}
                </div>
              </div>
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                task.status === "completed" ? "bg-green-100 text-green-700" :
                task.status === "in_progress" ? "bg-blue-100 text-blue-700" :
                "bg-gray-100 text-gray-700"
              }`}>
                {task.status === "in_progress" ? "In Progress" : task.status}
              </span>
            </div>

            {task.comments && task.comments.length > 0 && (
              <div className="mt-3 border-t pt-3 space-y-1">
                {task.comments.map((c) => (
                  <p key={c.id} className="text-sm text-gray-600"><span className="font-medium">{c.user_name || "User"}:</span> {c.content}</p>
                ))}
              </div>
            )}

            <div className="flex gap-2 mt-3">
              <input
                type="text"
                placeholder="Add comment..."
                value={commentText[task.id] || ""}
                onChange={(e) => setCommentText({ ...commentText, [task.id]: e.target.value })}
                className="flex-1 border rounded px-3 py-1 text-sm"
              />
              <button onClick={() => addComment(task.id)} className="bg-gray-600 text-white px-3 py-1 rounded text-sm hover:bg-gray-700">
                Comment
              </button>
            </div>
          </div>
        ))}
        {tasks.length === 0 && <p className="text-gray-400 text-center py-8">No tasks found</p>}
      </div>
    </div>
  );
}
