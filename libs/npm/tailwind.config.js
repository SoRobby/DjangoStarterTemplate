/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        '../../templates/**/*.{html, js}',
        '../../static/js/**/*.js',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
    ],
}

