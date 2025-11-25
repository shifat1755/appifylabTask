import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Login from "./pages/Login";
import Registration from "./pages/Registration";
import Feed from "./pages/Feed";
import ProtectedRoute from "./components/ProtectedRoute";

function RootRedirect() {
  const isAuthenticated = localStorage.getItem("authToken");
  return <Navigate to={isAuthenticated ? "/feed" : "/login"} replace />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<RootRedirect />} />
        <Route path="/register" element={<Registration />} />
        <Route
          path="/feed"
          element={
            <ProtectedRoute>
              <Feed />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
