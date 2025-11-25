import api from "./api";

export function togglePostLike(postId: number) {
    return api.post(`/posts/${postId}/like`)
        .then(res => res.data)
        .catch(() => {
            throw new Error("Failed to toggle like. Please try again later.");
        });
}
