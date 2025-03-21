import axios from "axios";
import { customAxios } from "./axiosCustom";


export const postQuery = async (user_input, category, flag) => {
  if (!flag) {
    console.error("❌ `flag` 값이 undefined입니다. 기본값 'select'로 설정합니다.");
    flag = "select";  // 기본값 설정
  }

  try {
    console.log(`📡 API 요청: { user_input: "${user_input}", category: "${category}", flag: "${flag}" }`);

    const response = await customAxios.post("/query", {
      user_input,
      category,
      flag, // ✅ flag 값을 명확하게 전달
    });

    console.log("📡 API 응답:", response.data); // ✅ 응답 로그 확인

    return response.data;
  } catch (error) {
    console.error("❌ API 요청 실패:", error);
    throw error;
  }
};


// json-server 테스트용
export const getRecipes = async () => {
  try {
    const response = await axios.get("http://localhost:5000/0");
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const postRecipes = async (user_input) => {
  try {
    const reponse = await customAxios.post("/recipes", user_input);
    return reponse.data;
  } catch (error) {
    throw error;
  }
};
