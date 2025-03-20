import axios from "axios";
import { customAxios } from "./axiosCustom";

// const response = await customAxios.post('/query', {user_input, category})
export const postQuery = async (user_input,category) => {
  try {

    console.log("🛠️ Sending request with:", { user_input,category }); // ✅ 디버깅 추가
    const response = await customAxios.post("/query", { user_input,category });
    console.log("✅ Response received:", response.data);  // ✅ 응답 로그 추가

    return response.data;
  } catch (error) {
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
