export type Sentiment = "Positive" | "Negative";

export interface Feedback {
  id: number;
  text: string;
  sentiment: Sentiment;
  score: number;
  created_at: string;
}

export interface FeedbackResponse {
  sentiment: Sentiment;
  score: number;
}

export interface FeedbackListResponse {
  feedbacks: Feedback[];
}

export interface FilteredFeedbackResponse {
  sentiment: string;
  count: number;
  feedbacks: Feedback[];
}

export interface DeleteResponse {
  message: string;
}
