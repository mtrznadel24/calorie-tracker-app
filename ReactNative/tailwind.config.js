/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        primary: "#3B5BDB",

        accent: "#5EEAD4",

        light: {
          50:  "#FFFFFF",
          100: "#F8F9FB",
          200: "#EEF1F5",
          300: "#D9DEE5",
        },

        dark: {
          900: "#0D0D0D",
          800: "#161616",
          700: "#1F1F1F",
          600: "#2A2A2A",
          500: "#3A3A3A",
        },

        text: {
          light: "#EDEDED",
          muted: "#A1A1A1",
          dark: "#222222",
        },

        state: {
          success: "#4ADE80",
          warning: "#FBBF24",
          error: "#EF4444",
        },
      },
    },
  },
  plugins: [],
}