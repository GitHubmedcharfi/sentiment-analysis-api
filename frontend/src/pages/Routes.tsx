import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import Home from "./Home";
import FeedbackPage from "./Feedback";
import StatsPage from "./Stats";
import "../styles/Routes.css";

const AppRoutes = () => {
  return (
    <Router>
      <nav className="nav-bar">
        <NavLink to="/" end className={({ isActive }) => isActive ? "active" : ""}>
          Home
        </NavLink>
        <NavLink to="/feedbacks" className={({ isActive }) => isActive ? "active" : ""}>
          Feedbacks
        </NavLink>
        <NavLink to="/stats" className={({ isActive }) => isActive ? "active" : ""}>
          Statistics
        </NavLink>
      </nav>
      <div className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/feedbacks" element={<FeedbackPage />} />
          <Route path="/stats" element={<StatsPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default AppRoutes;
