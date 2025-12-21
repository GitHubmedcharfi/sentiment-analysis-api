import { useEffect, useState } from "react";
import Swal from "sweetalert2";
import { getAllFeedbacks, deleteFeedback, filterFeedbacks, deleteAllFeedbacks } from "../services/api/feedback.service";
import "../styles/Feedback.css";

interface Feedback {
  id: number;
  text: string;
  sentiment: string;
  score: number;
  created_at: string;
}

type FilterType = "all" | "positive" | "negative";

const FeedbackPage = () => {
  const [feedbacks, setFeedbacks] = useState<Feedback[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState<FilterType>("all");
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const fetchFeedbacks = async (filterType: FilterType = filter) => {
    setError("");
    setLoading(true);
    try {
      let res;
      if (filterType === "all") {
        res = await getAllFeedbacks();
        setFeedbacks(res.feedbacks);
      } else {
        res = await filterFeedbacks(filterType);
        setFeedbacks(res.feedbacks);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load feedbacks");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    const feedback = feedbacks.find(f => f.id === id);
    const feedbackText = feedback?.text 
      ? (feedback.text.length > 50 ? feedback.text.substring(0, 50) + "..." : feedback.text)
      : "this feedback";

    const result = await Swal.fire({
      title: "Delete Feedback?",
      html: `
        <p>Are you sure you want to delete this feedback?</p>
        <p style="font-style: italic; color: #666; margin-top: 10px;">"${feedbackText}"</p>
      `,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#f44336",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Yes, delete it!",
      cancelButtonText: "Cancel",
    });

    if (!result.isConfirmed) {
      return;
    }

    setDeletingId(id);
    try {
      await deleteFeedback(id);
      await fetchFeedbacks();
      
      Swal.fire({
        icon: "success",
        title: "Deleted!",
        text: "Feedback has been deleted successfully.",
        confirmButtonColor: "#4CAF50",
        timer: 2000,
        timerProgressBar: true,
      });
    } catch (err: any) {
      const errorMessage = err.message || "Delete failed";
      setError(errorMessage);
      
      Swal.fire({
        icon: "error",
        title: "Delete Failed",
        text: errorMessage,
        confirmButtonColor: "#f44336",
      });
    } finally {
      setDeletingId(null);
    }
  };

  const handleDeleteAll = async () => {
    const result = await Swal.fire({
      title: "Delete All Feedbacks?",
      html: `
        <p>Are you sure you want to delete <strong>ALL ${feedbacks.length} feedbacks</strong>?</p>
        <p style="color: #f44336; font-weight: bold; margin-top: 15px;">⚠️ This action cannot be undone!</p>
      `,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#f44336",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Yes, delete all!",
      cancelButtonText: "Cancel",
      reverseButtons: true,
    });

    if (!result.isConfirmed) {
      return;
    }

    try {
      await deleteAllFeedbacks();
      await fetchFeedbacks();
      
      Swal.fire({
        icon: "success",
        title: "All Deleted!",
        text: `All ${feedbacks.length} feedbacks have been deleted successfully.`,
        confirmButtonColor: "#4CAF50",
        timer: 3000,
        timerProgressBar: true,
      });
    } catch (err: any) {
      const errorMessage = err.message || "Failed to delete all feedbacks";
      setError(errorMessage);
      
      Swal.fire({
        icon: "error",
        title: "Delete Failed",
        text: errorMessage,
        confirmButtonColor: "#f44336",
      });
    }
  };

  const handleFilterChange = (newFilter: FilterType) => {
    setFilter(newFilter);
    fetchFeedbacks(newFilter);
  };

  useEffect(() => {
    fetchFeedbacks();
  }, []);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="feedback-container">
      <h1>Feedback Management</h1>
      
      <div className="controls">
        <div className="filter-buttons">
          <button 
            className={filter === "all" ? "active" : ""}
            onClick={() => handleFilterChange("all")}
          >
            All ({feedbacks.length})
          </button>
          <button 
            className={filter === "positive" ? "active" : ""}
            onClick={() => handleFilterChange("positive")}
          >
            Positive
          </button>
          <button 
            className={filter === "negative" ? "active" : ""}
            onClick={() => handleFilterChange("negative")}
          >
            Negative
          </button>
        </div>
        
        {feedbacks.length > 0 && (
          <button 
            className="delete-all-btn"
            onClick={handleDeleteAll}
          >
            Delete All
          </button>
        )}
      </div>

      {error && <div className="error-message">{error}</div>}
      
      {loading ? (
        <div className="loading">Loading feedbacks...</div>
      ) : feedbacks.length === 0 ? (
        <div className="empty-state">
          <p>No feedbacks found.</p>
          {filter !== "all" && (
            <button onClick={() => handleFilterChange("all")}>
              Show All Feedbacks
            </button>
          )}
        </div>
      ) : (
        <ul className="feedback-list">
          {feedbacks.map((f) => (
            <li key={f.id} className={f.sentiment.toLowerCase()}>
              <div className="feedback-content">
                <p className="feedback-text">{f.text}</p>
                <div className="feedback-meta">
                  <span className={`sentiment-badge sentiment-${f.sentiment.toLowerCase()}`}>
                    {f.sentiment}
                  </span>
                  <span className="score-badge">Score: {f.score.toFixed(2)}</span>
                  <span className="date-badge">{formatDate(f.created_at)}</span>
                </div>
              </div>
              <button 
                className="delete-btn"
                onClick={() => handleDelete(f.id)}
                disabled={deletingId === f.id}
              >
                {deletingId === f.id ? "Deleting..." : "Delete"}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FeedbackPage;
