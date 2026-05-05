import { Outlet, Link, useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { Ship, Wrench, AlertTriangle, BarChart3, LogOut } from "lucide-react";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const isActive = (path: string) => location.pathname === path || location.pathname.startsWith(path + "/");

  const linkClass = (path: string) =>
    `flex items-center gap-2 px-3 py-2 rounded text-sm font-medium transition-colors ${
      isActive(path) ? "bg-blue-700 text-white" : "text-blue-100 hover:bg-blue-600"
    }`;

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <nav className="w-64 bg-blue-800 text-white flex flex-col">
        <div className="p-4 border-b border-blue-700">
          <Link to="/" className="flex items-center gap-2">
            <Ship size={24} />
            <span className="font-bold text-lg">Fathom Marine</span>
          </Link>
        </div>
        <div className="p-3 space-y-1 flex-1">
          <Link to="/" className={linkClass("/")}>
            <BarChart3 size={18} /> Dashboard
          </Link>
          <Link to="/maintenance" className={linkClass("/maintenance")}>
            <Wrench size={18} /> Maintenance
          </Link>
          <Link to="/drills" className={linkClass("/drills")}>
            <AlertTriangle size={18} /> Safety Drills
          </Link>
          {user?.role === "admin" && (
            <Link to="/ships" className={linkClass("/ships")}>
              <Ship size={18} /> Ships
            </Link>
          )}
        </div>
        <div className="p-3 border-t border-blue-700">
          <div className="text-xs text-blue-200 mb-2">
            <p className="font-medium">{user?.name}</p>
            <p className="capitalize">{user?.role}</p>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-2 text-sm text-blue-200 hover:text-white w-full">
            <LogOut size={16} /> Sign Out
          </button>
        </div>
      </nav>
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}
