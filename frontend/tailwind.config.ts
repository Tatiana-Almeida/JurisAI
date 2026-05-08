import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class", ".dark"],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./hooks/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
    "./stores/**/*.{ts,tsx}",
    "./types/**/*.{ts,tsx}",
    "./tests/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        jurisai: {
          50: "#eef6ff",
          100: "#d9ebff",
          200: "#bcdcfe",
          300: "#8dc4fd",
          400: "#57a2fb",
          500: "#2d83f5",
          600: "#1767ea",
          700: "#1652d6",
          800: "#1945ae",
          900: "#1a3c88",
          950: "#122656",
        },
      },
      boxShadow: {
        panel: "0 10px 30px -18px rgba(15, 23, 42, 0.35)",
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
      },
      backgroundImage: {
        "jurisai-grid":
          "radial-gradient(circle at top, rgba(45,131,245,0.18), transparent 36%), linear-gradient(180deg, rgba(248,250,252,0.92), rgba(255,255,255,0.98))",
      },
    },
  },
};

export default config;
