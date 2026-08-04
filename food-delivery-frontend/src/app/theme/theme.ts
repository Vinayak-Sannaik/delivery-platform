import { createTheme } from "@mantine/core";

export const theme = createTheme({
  primaryColor: "blue",
  primaryShade: 6,

  defaultRadius: "md",

  fontFamily:
    "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",

  headings: {
    fontFamily:
      "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
  },

  colors: {
    blue: [
      "#eef4ff",
      "#d9e7ff",
      "#b3ceff",
      "#80adff",
      "#4d8cff",
      "#2563eb",
      "#1d4ed8",
      "#1e40af",
      "#1e3a8a",
      "#172554",
    ],
  },
});