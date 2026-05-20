import axios from "axios";
import { API_BASE_URL } from "./api-base";

const api = axios.create({
    baseURL: API_BASE_URL,
    withCredentials: true,
    timeout: 30_000,
});

export default api;
