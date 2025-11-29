interface Post {
    id: number;
    content: string;
    image_url: string | null;
    visibility: string;
    likes_count: number;
    comments_count: number;
    created_at: string;
    author?: {
        id: number;
        first_name: string;
        last_name: string;
        email: string;
        avatar_url: string | null;
    };
}
export type { Post };