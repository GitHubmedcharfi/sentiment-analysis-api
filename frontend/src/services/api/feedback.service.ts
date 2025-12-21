import {
  FeedbackListResponse,
  FilteredFeedbackResponse,
  DeleteResponse,
} from "../../types/feedback";
import { API_BASE_URL } from "./config";

export const getAllFeedbacks = async (): Promise<FeedbackListResponse> => {
  const res = await fetch(`${API_BASE_URL}/api/feedbacks/`);
  if (!res.ok) throw new Error("Failed to fetch feedbacks");
  return res.json();
};

export const filterFeedbacks = async (
  sentiment: "positive" | "negative"
): Promise<FilteredFeedbackResponse> => {
  const res = await fetch(
    `${API_BASE_URL}/api/feedbacks/filter/${sentiment}`
  );
  if (!res.ok) throw new Error("Failed to filter feedbacks");
  return res.json();
};

export const deleteFeedback = async (
  id: number
): Promise<DeleteResponse> => {
  const res = await fetch(`${API_BASE_URL}/api/feedbacks/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete feedback");
  return res.json();
};

export const deleteAllFeedbacks = async (): Promise<DeleteResponse> => {
  const res = await fetch(`${API_BASE_URL}/api/feedbacks/`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete all feedbacks");
  return res.json();
};
