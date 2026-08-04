import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute() {
  const authenticated = true;

  if (!authenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}