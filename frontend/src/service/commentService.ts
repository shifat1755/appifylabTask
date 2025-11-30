import api from "./axiosApi";

export function getPostComments(postId: number, skip: number = 0, limit: number = 50) {
    return api.get(`/posts/${postId}/comments`, {
        params: {
            skip,
            limit,
            sort_by: "newest",
            top_level_only: true,
        },
    })
        .then(res => res.data)
        .catch((error) => {
            console.error("Error fetching comments:", error);
            throw error;
        });
}

export function createComment(postId: number, content: string) {
    return api.post(`/posts/${postId}/comments`, {
        content,
    })
        .then(res => res.data)
        .catch((error) => {
            console.error("Error creating comment:", error);
            // Re-throw to let the component handle it
            throw error;
        });
}
