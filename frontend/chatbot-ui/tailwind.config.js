/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,jsx,ts,tsx}", 
  ],
  theme: {
    extend: {
      keyframes: {
        fadein: {
          "0%": {
            opacity: "0",
            transform: "translateY(-10px)",
          },
          "100%": {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
        fadeout: {
          "0%": {
            opacity: "1",
          },
          "100%": {
            opacity: "0",
          },
        },
        fadeinCategory: {
          "0%": {
            opacity: "0",
            transform: "translateY(10px)",
          },
          "100%": {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
        fadeoutCategory: {
          "0%": {
            opacity: "1",
            transform: "translateY(0)",
          },
          "100%": {
            opacity: "0",
            transform: "translateY(10px)",
          },
        },
        moveDown: {
          "0%": { transform: "translateY(0px)" },
          "100%": { transform: "translateY(50px)" },
        },
        loadingDots: {
          '0%, 80%, 100%': { transform: 'scale(0)' },
          '40%': { transform: 'scale(1)' },
        },
        bounceUp: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-8px)' },
        },
      },
      animation: {
        fadein: "fadein 1s",
        fadeout: "fadeout 1s",
        fadeinCategory: "fadeinCategory 1s",
        fadeoutCategory: "fadeoutCategory 1s",
        moveDown: "moveDown 0.5s ease-in-out forwards",
        loadingDots: 'loadingDots 1.4s infinite ease-in-out',
        bounceUp: 'bounceUp 0.6s infinite',
        bounceUpDelayed1: 'bounceUp 0.6s infinite 0.1s',
        bounceUpDelayed2: 'bounceUp 0.6s infinite 0.2s',
      },
    },
  },
  plugins: [
    require("daisyui"), // DaisyUI 플러그인 배열로 설정
  ],
}

