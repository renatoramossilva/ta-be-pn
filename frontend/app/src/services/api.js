import axios from "axios";

const API_URL = "http://localhost:8000"; // backend URL

const getMobileCoverage = async (address) => {
    try {
        console.log("API request:", `${API_URL}/coverage?address=${address}`);
        const response = await axios.get(`${API_URL}/coverage?address=${address}`);
        return response.data;
    } catch (error) {
        console.error("Error:", error);
        return null;
    }
};

export default getMobileCoverage;
