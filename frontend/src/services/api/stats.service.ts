import { StatsResponse } from "../../types/stats";
import { API_BASE_URL } from "./config";

export const getStats = async (): Promise<StatsResponse> => {
  const res = await fetch(`${API_BASE_URL}/api/stats/`);
  if (!res.ok) throw new Error("Failed to fetch statistics");
  return res.json();
};
