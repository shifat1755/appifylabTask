import axios from "axios"


axios.defaults.withCredentials = true;

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
    headers: {
        "Content-Type": "application/json",
    },
})

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("authToken")
    console.log("Attaching_token_to_request:", token)
    if (token) {
        config.headers["Authorization"] = `Bearer ${token}`
    }
    return config
})

api.interceptors.response.use((response) => response,
    async (error) => {
        const originalreq = error.config;
        if (error.response?.status === 401 && !originalreq._retry) {
            originalreq._retry = true;
            try {
                const res = await axios.post('http://localhost:8000/api/auth/refresh', {}, { withCredentials: true });
                localStorage.setItem("authToken", res.data.access_token);
                return api(originalreq);
            }
            catch (err) {
                console.log("Refresh_token_failed:", err);
                localStorage.removeItem("authToken");
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);

    });

export default api;