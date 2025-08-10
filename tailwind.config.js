/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./App.tsx",
    "./components/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    fontFamily: {
      sans: ["Helvetica", "Arial", "sans-serif"],
    },
    extend: {
      colors: {
        primary: "#030213",
        "primary-foreground": "#ffffff",
        secondary: "#f8f9fa",
        "secondary-foreground": "#030213",
        muted: "#ececf0",
        "muted-foreground": "#717182",
        accent: "#e9ebef",
        "accent-foreground": "#030213",
        destructive: "#d4183d",
        "destructive-foreground": "#ffffff",
        border: "#e5e7eb",
        input: "transparent",
        "input-background": "#f3f3f5",
        ring: "#e5e7eb",
      },
      fontSize: {
        base: "14px",
      },
      fontWeight: {
        normal: "400",
        medium: "500",
      },
      borderRadius: {
        lg: "0.625rem",
        md: "calc(0.625rem - 2px)",
        sm: "calc(0.625rem - 4px)",
        xl: "calc(0.625rem + 4px)",
      },
    },
  },
  darkMode: "class",
  plugins: [],
};
