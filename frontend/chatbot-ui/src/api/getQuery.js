import axios from "axios";
import { customAxios } from "./axiosCustom"

export const postQuery = async ( user_input, category ) => {
    try {
        // const response = await customAxios.post('/query', {user_input, category})
        const response = await customAxios.post('/query', {user_input});
        return response.data;
    } catch (error) {
        throw error;
    }
}

// json-server 테스트용
export const getRecipes = async () => {
    try {
        const response = await axios.get('http://localhost:5000/0')
        return response.data
    } catch (error) {
        throw error
    }
}

export const postRecipes = async (user_input) => {
    try {
        const reponse = await customAxios.post('/recipes', user_input)
        return reponse.data
    } catch (error) {
        throw error
    }
}