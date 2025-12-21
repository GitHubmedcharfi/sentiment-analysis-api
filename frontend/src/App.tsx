import { useEffect, useState } from "react";
import { getStats } from "./services/api/stats.service";
import { predictSentiment } from "./services/api/sentiment.service";

function App() {
  const [stats, setStats] = useState<any>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getStats()
      .then((data) => setStats(data))
      .catch((err) => setError("Stats Error: " + err.message));

    predictSentiment("I love this product!")
      .then((data) => setPrediction(data))
      .catch((err) => setError("Prediction Error: " + err.message));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Sentiment Analysis Frontend - Testing API</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>Stats:</h2>
      {stats ? (
        <pre>{JSON.stringify(stats, null, 2)}</pre>
      ) : (
        <p>Loading stats...</p>
      )}

      <h2>Prediction:</h2>
      {prediction ? (
        <pre>{JSON.stringify(prediction, null, 2)}</pre>
      ) : (
        <p>Loading prediction...</p>
      )}
    </div>
  );
}

export default App;
