import axios from "axios";

const api = axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_API_URI }`,
    withCredentials: true,
});

export default api;