export interface User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    phone: string | null;
    avatar_url: string;
    bio: string | null;
    created_at: string;
    is_active: boolean;
    is_verified: boolean;
    updated_at: string;
    last_login: string | null;
}