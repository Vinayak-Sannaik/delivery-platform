import { createBrowserRouter } from "react-router-dom";

import BlankLayout from "../layouts/BlankLayout";
import AuthLayout from "../layouts/AuthLayout";
import AppLayout from "../layouts/AppLayout";
import ProtectedRoute from "./ProtectedRoute";

import LoginPage from "../../modules/auth/pages/LoginPage";
import RegisterPage from "../../modules/auth/pages/RegisterPage";

import WarmupPage from "../../modules/health/pages/WarmupPage";
import DashboardPage from "../../modules/dashboard/pages/DashboardPage";

import RestaurantsPage from "../../modules/restaurants/pages/RestaurantsPage";
import RestaurantDetailsPage from "../../modules/restaurants/pages/RestaurantDetailsPage";
import ManageRestaurantsPage from "../../modules/restaurants/pages/ManageRestaurantsPage"

import RestaurantFormPage from "../../modules/restaurants/pages/RestaurantFormPage";

import CartPage from "../../modules/cart/pages/CartPage";
import OrdersPage from "../../modules/orders/pages/OrdersPage";

import RestaurantOrdersPage from "../../modules/orders/pages/RestaurantOrdersPage";
import OwnerRestaurantsPage from "../../modules/orders/pages/OwnerRestaurantsPage";

import DeliveryDashboardPage from "../../modules/delivery/pages/DeliveryDashboardPage";
import AdminDeliveriesPage from "../../modules/delivery/pages/AdminDeliveriesPage";

export const router = createBrowserRouter([
  // --------------------------------------------------
  // Warmup
  // --------------------------------------------------
  {
    element: <BlankLayout />,
    children: [
      {
        path: "/",
        element: <WarmupPage />,
      },
    ],
  },

  // --------------------------------------------------
  // Authentication
  // --------------------------------------------------
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

  // --------------------------------------------------
  // Protected Application
  // --------------------------------------------------
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          // Dashboard
          {
            path: "/dashboard",
            element: <DashboardPage />,
          },

          // Customer
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

          // Restaurant Owner
          {
            path: "/owner/restaurants",
            element: <OwnerRestaurantsPage />,
          },
          {
            path: "/owner/restaurants/:restaurantId/orders",
            element: <RestaurantOrdersPage />,
          },
{

  path:"/admin/restaurants",
  element: <ManageRestaurantsPage />

},
{
  path:"/admin/restaurants/new",
            element: <RestaurantFormPage />,
},
{
  path:"/admin/restaurants/:id/edit",
            element: <RestaurantFormPage />,
},

          // Delivery Partner
          {
            path: "/delivery",
            element: <DeliveryDashboardPage />,
          },

          // Admin
          {
            path: "/admin/deliveries",
            element: <AdminDeliveriesPage />,
          },
        ],
      },
    ],
  },
]);