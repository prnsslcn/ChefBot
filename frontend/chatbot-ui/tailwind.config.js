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
        moveDown: {
          "0%": { transform: "translateY(0px)" },
          "100%": { transform: "translateY(50px)" },
        },
      },
      animation: {
        fadein: "fadein 1s",
        fadeout: "fadeout 1s",
        moveDown: "moveDown 0.5s ease-in-out forwards",
      },
    },
  },
  plugins: [
    require("daisyui"), // DaisyUI 플러그인 배열로 설정
  ],
}

