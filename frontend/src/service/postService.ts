import api from "./api";

export function createPost(data: any) {
    return api.post("/posts", data)
        .then(res => res.data)
        .catch(() => {
            throw new Error("Failed to create post. Please try again later.");
        });
}