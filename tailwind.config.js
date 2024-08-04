/** @type {import('tailwindcss').Config} */
export default {
  content: ["./app/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

