export interface Ship {
  id: string;
  name: string;
  created_at: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: "admin" | "crew";
  ship_id: string | null;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export type TaskStatus = "pending" | "in_progress" | "completed";

export interface MaintenanceTask {
  id: string;
  title: string;
  description: string | null;
  status: TaskStatus;
  due_date: string;
  ship_id: string;
  assigned_to: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
  ship_name?: string;
  assigned_user_name?: string;
  comments?: TaskComment[];
}

export interface TaskComment {
  id: string;
  task_id: string;
  user_id: string;
  content: string;
  created_at: string;
  user_name?: string;
}

export type DrillStatus = "scheduled" | "completed" | "missed";

export interface SafetyDrill {
  id: string;
  drill_type: string;
  description: string | null;
  scheduled_date: string;
  status: DrillStatus;
  ship_id: string;
  created_by: string;
  created_at: string;
  ship_name?: string;
}

export interface ComplianceStats {
  maintenance_pct: number;
  drill_pct: number;
  overall_pct: number;
  overdue_tasks: number;
  missed_drills: number;
}

export interface ShipCompliance {
  ship_id: string;
  ship_name: string;
  maintenance_pct: number;
  drill_pct: number;
  overall_pct: number;
  overdue_tasks: number;
  missed_drills: number;
}
