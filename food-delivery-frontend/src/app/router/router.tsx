import { createBrowserRouter } from "react-router-dom";

import BlankLayout from "../layouts/BlankLayout";
import AuthLayout from "../layouts/AuthLayout";
import AppLayout from "../layouts/AppLayout";

import LoginPage from "../../modules/auth/pages/LoginPage";
import RegisterPage from "../../modules/auth/pages/RegisterPage";

import WarmupPage from "../../modules/health/pages/WarmupPage";
import DashboardPage from "../../modules/dashboard/pages/DashboardPage";

import ProtectedRoute from "./ProtectedRoute";

export const router = createBrowserRouter([
  // Warmup
  {
    element: <BlankLayout />,
    children: [
      {
        path: "/",
        element: <WarmupPage />,
      },
    ],
  },

  // Authentication
  {
    element: <AuthLayout />,
    children: [
      {
        path: "/login",
        element: <LoginPage />,
      },
      {
        path: "/register",
        element: <RegisterPage />,
      },
    ],
  },

  // Application
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          {
            path: "/dashboard",
            element: <DashboardPage />,
          },
        ],
      },
    ],
  },
]);