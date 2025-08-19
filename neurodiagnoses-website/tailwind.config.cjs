/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{astro,html,md,mdx,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#2342FF',
        accent:  '#0CD3A0',
        dark:    '#0B1020',
        light:   '#F8FAFF'
      },
      borderRadius: {
        '2xl': '1rem', // 16px
      }
    }
  },
  plugins: [],
};