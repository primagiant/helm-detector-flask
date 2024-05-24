/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
       colors: {
        primary: '#eaeae0',
        active: '#afedae',
        inactive: '#c6d3f5'
      }
    },
  },
  plugins: [],
}

