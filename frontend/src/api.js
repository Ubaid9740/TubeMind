import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

// 👇 The word 'export' is REQUIRED here!
export const summarizeVideo = async (url) => {
    try {
        const response = await axios.post(`${API_URL}/summarize`, { url });
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};