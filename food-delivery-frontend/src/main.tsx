import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";

import "./app/theme/globals.css";

import QueryProvider from "./app/providers/QueryProvider";
import MantineProvider from "./app/providers/MantineProvider";

import App from "./App";

import React from "react";
import ReactDOM from "react-dom/client";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryProvider>
      <MantineProvider>
        <App />
      </MantineProvider>
    </QueryProvider>
  </React.StrictMode>
);