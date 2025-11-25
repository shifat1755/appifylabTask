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

export function getPosts(skip: number = 0, limit: number = 20, sortBy: string = "newest") {
    return api.get("/posts", {
        params: {
            skip,
            limit,
            sort_by: sortBy,
        },
    })
        .then(res => res.data)
        .catch(() => {
            throw new Error("Failed to fetch posts. Please try again later.");
        });
}