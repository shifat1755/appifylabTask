import api from "./axiosApi";

export async function userInfo() {
    try {
        const res = await api.get("users/me")
        return res.data
    }
    catch (err) {
        throw new Error("error on fetching user")
    }
}