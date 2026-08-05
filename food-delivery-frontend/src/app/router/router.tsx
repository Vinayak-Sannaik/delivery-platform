import { createBrowserRouter } from "react-router-dom";

import BlankLayout from "../layouts/BlankLayout";
import AuthLayout from "../layouts/AuthLayout";
import AppLayout from "../layouts/AppLayout";

import LoginPage from "../../modules/auth/pages/LoginPage";
import RegisterPage from "../../modules/auth/pages/RegisterPage";

import WarmupPage from "../../modules/health/pages/WarmupPage";
import DashboardPage from "../../modules/dashboard/pages/DashboardPage";

import ProtectedRoute from "./ProtectedRoute";

import RestaurantsPage from "../../modules/restaurants/pages/RestaurantsPage";
import RestaurantDetailsPage from "../../modules/restaurants/pages/RestaurantDetailsPage";
import CartPage from "../../modules/cart/pages/CartPage";
import OrdersPage from "../../modules/orders/pages/OrdersPage";
import RestaurantOrdersPage from "../../modules/orders/pages/RestaurantOrdersPage";
import OwnerRestaurantsPage from "../../modules/orders/pages/OwnerRestaurantsPage";
import DeliveryDashboardPage from "../../modules/delivery/pages/DeliveryDashboardPage"
import AdminDeliveriesPage from "../../modules/delivery/pages/AdminDeliveriesPage"

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
          {
            path: "/restaurants",
            element: <RestaurantsPage />,
          },
          {
            path: "/restaurants/:id",
            element: <RestaurantDetailsPage />,
          },
          {
            path: "/cart",
            element: <CartPage />,
          },
          {
            path: "/orders",
            element: <OrdersPage />,
          },
          {
            path: "/owner/restaurants",
            element: <OwnerRestaurantsPage />,
          },
          {
            path: "/owner/restaurants/:restaurantId/orders",
            element: <RestaurantOrdersPage />,
          },
          {
  path: "/delivery",
  element: <DeliveryDashboardPage />,
},
{
  path: "/admin/deliveries",
  element: <AdminDeliveriesPage />,
}
        ],
      },
    ],
  },
]);
