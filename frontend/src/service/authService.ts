import api from "./api";


export function login(email: string, password: string) {
    return api.post("/auth/login", { email, password })
        .then(res => res.data)
        .catch((err: any) => {
            if (err.response?.status === 401) {
                throw new Error("Wrong email or password");
            }
            throw new Error("Something went wrong. Please try again later.");
        });
}

export async function register(data: any) {
    const response = await api.post("/auth/signup", data);
    return response.data;
}

export async function logout() {
    const response = await api.post("/auth/logout");
    localStorage.removeItem("authToken");
    return response.data;
}