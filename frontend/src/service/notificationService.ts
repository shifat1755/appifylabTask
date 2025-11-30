import api from "./axiosApi";

export interface Notification {
  id: string;
  user_id: number;
  type: string;
  message: string;
  post_id?: number;
  comment_id?: number;
  actor_id?: number;
  created_at: string;
}

export interface NotificationList {
  notifications: Notification[];
  unread_count: number;
}

export function getNotifications(): Promise<NotificationList> {
  return api
    .get("/notifications")
    .then((res) => res.data)
    .catch((error) => {
      console.error("Error fetching notifications:", error);
      throw error;
    });
}
