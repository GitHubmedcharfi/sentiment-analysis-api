import { useState } from "react";
import Swal from "sweetalert2";
import { predictSentiment } from "../services/api/sentiment.service";
import "../styles/Home.css";

const Home = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState<{ sentiment: string; score: number } | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) {
      Swal.fire({
        icon: "warning",
        title: "Empty Text",
        text: "Please enter some text to analyze",
        confirmButtonColor: "#4CAF50",
      });
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await predictSentiment(text.trim());
      setResult(res);
      
      // Show success notification
      Swal.fire({
        icon: "success",
        title: "Analysis Complete!",
        html: `
          <div style="text-align: left; margin-top: 10px;">
            <p><strong>Sentiment:</strong> <span style="color: ${res.sentiment === 'Positive' ? '#4CAF50' : '#f44336'}">${res.sentiment}</span></p>
            <p><strong>Confidence Score:</strong> ${res.score.toFixed(2)}</p>
          </div>
        `,
        confirmButtonColor: "#4CAF50",
        timer: 3000,
        timerProgressBar: true,
      });
    } catch (err: any) {
      const errorMessage = err.message || "Something went wrong. Please try again.";
      setError(errorMessage);
      
      // Show error notification
      Swal.fire({
        icon: "error",
        title: "Analysis Failed",
        text: errorMessage,
        confirmButtonColor: "#f44336",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      handleSubmit();
    }
  };

  return (
    <div className="home-container">
      <h1>Sentiment Analysis</h1>
      <p className="subtitle">Enter text below to analyze its sentiment</p>
      
      <div className="input-group">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your feedback here... (Ctrl+Enter to submit)"
          disabled={loading}
          rows={6}
        />
        <button 
          onClick={handleSubmit} 
          disabled={loading || !text.trim()}
          className="analyze-btn"
        >
          {loading ? "Analyzing..." : "Analyze Sentiment"}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}
      
      {result && (
        <div className={`result ${result.sentiment.toLowerCase()}`}>
          <div className="result-header">
            <h3>Analysis Result</h3>
          </div>
          <div className="result-content">
            <div className="result-item">
              <span className="label">Sentiment:</span>
              <span className={`value sentiment-${result.sentiment.toLowerCase()}`}>
                {result.sentiment}
              </span>
            </div>
            <div className="result-item">
              <span className="label">Confidence Score:</span>
              <span className="value score">{result.score.toFixed(2)}</span>
            </div>
            <div className="score-bar">
              <div 
                className="score-fill" 
                style={{ width: `${result.score * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;
