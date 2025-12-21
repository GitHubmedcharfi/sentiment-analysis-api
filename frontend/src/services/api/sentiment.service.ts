import { FeedbackResponse } from "../../types/feedback";
import { API_BASE_URL } from "./config";

export const predictSentiment = async (
  text: string
): Promise<FeedbackResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error("Failed to predict sentiment");
  }

  return response.json();
};
