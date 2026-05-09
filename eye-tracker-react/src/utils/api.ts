const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface FocusLogPayload {
  session_id: number;
  timestamp: string;
  status: "focused" | "distracted" | "no_face";
  duration_ms: number;
  gaze_x?: number;
  gaze_y?: number;
  reason?: string;
}

export async function createSession(deviceId: string): Promise<{ id: number }> {
  const response = await fetch(`${API_BASE_URL}/sessions?device_id=${encodeURIComponent(deviceId)}`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to create session");
  return response.json();
}

export async function endSession(sessionId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}/end`, {
    method: "POST",
  });
  if (!response.ok) throw new Error("Failed to end session");
}

export async function logFocus(payload: FocusLogPayload): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/sessions/${payload.session_id}/logs`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) throw new Error("Failed to log focus");
}

export async function getStats(deviceId: string): Promise<{
  total_sessions: number;
  total_focus_time: number;
  total_distracted_time: number;
  focus_percentage: number;
  average_session_duration: number;
}> {
  const response = await fetch(`${API_BASE_URL}/stats/${encodeURIComponent(deviceId)}`);
  if (!response.ok) throw new Error("Failed to get stats");
  return response.json();
}

export function getDeviceId(): string {
  let deviceId = localStorage.getItem("eye_tracker_device_id");
  if (!deviceId) {
    deviceId = crypto.randomUUID();
    localStorage.setItem("eye_tracker_device_id", deviceId);
  }
  return deviceId;
}