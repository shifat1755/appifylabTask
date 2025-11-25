import api from "./api";

export function createPost(data: FormData) {
    return api.post("/posts", data, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    })
        .then(res => res.data)
        .catch(() => {
            throw new Error("Failed to create post. Please try again later.");
        });
}