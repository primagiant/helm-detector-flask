/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html"],
    theme: {
        extend: {
            colors: {
                primary: '#eaeae0',
                active: '#afedae',
                activeHover: '#a2eaa1',
                inactive: '#c6d3f5'
            }
        },
    },
    plugins: [],
}

