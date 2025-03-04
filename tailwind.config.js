/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'green-primary': '#00E676',
        'purple-primary': '#9C27B0',
        'orange-primary': '#FF5722',
        'neon-purple': '#8A2BE2',
        'dark-purple': '#1E0033',
      },
      aspectRatio: {
        '1/1': '1 / 1',
      },
      backgroundColor: {
        'dark-purple-gradient': 'linear-gradient(to bottom, #1E0033, #0A0015)',
      },
    },
  },
  plugins: [],
};