export interface Comment {
    id: number;
    content: string;
    author_id: number;
    likes_count: number;
    created_at: string;
    author?: {
        id: number;
        first_name: string;
        last_name: string;
        email: string;
        avatar_url: string | null;
    };
}