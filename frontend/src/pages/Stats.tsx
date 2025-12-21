import { useEffect, useState } from "react";
import { getStats } from "../services/api/stats.service";
import "../styles/Stats.css";
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from "recharts";

const COLORS = ["#00C49F", "#FF8042"]; // Green for positive, orange for negative

const StatsPage = () => {
  const [stats, setStats] = useState<any>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getStats();
        setStats(data);
      } catch (err: any) {
        setError(err.message || "Failed to fetch stats");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="stats-container">
        <div className="loading">Loading statistics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="stats-container">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  if (!stats || stats.total_feedbacks === 0) {
    return (
      <div className="stats-container">
        <h1>Feedback Statistics</h1>
        <div className="empty-state">
          <p>No feedback data available yet.</p>
          <p>Start analyzing text to see statistics here!</p>
        </div>
      </div>
    );
  }

  const pieData = [
    { name: "Positive", value: stats.positive, percentage: stats.positive_percentage },
    { name: "Negative", value: stats.negative, percentage: stats.negative_percentage },
  ];

  const barData = [
    { name: "Positive", value: stats.positive, percentage: stats.positive_percentage },
    { name: "Negative", value: stats.negative, percentage: stats.negative_percentage },
  ];

  return (
    <div className="stats-container">
      <h1>Feedback Statistics</h1>
      
      <div className="stats-summary">
        <div className="stat-card total">
          <div className="stat-value">{stats.total_feedbacks}</div>
          <div className="stat-label">Total Feedbacks</div>
        </div>
        <div className="stat-card positive">
          <div className="stat-value">{stats.positive}</div>
          <div className="stat-label">Positive ({stats.positive_percentage.toFixed(1)}%)</div>
        </div>
        <div className="stat-card negative">
          <div className="stat-value">{stats.negative}</div>
          <div className="stat-label">Negative ({stats.negative_percentage.toFixed(1)}%)</div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-container">
          <h2>Sentiment Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                fill="#8884d8"
                label={({ name, percent }: any) => `${name}: ${(percent * 100).toFixed(1)}%`}
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-container">
          <h2>Comparison Chart</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default StatsPage;
