import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { togglePostLike } from "../../service/likeService";
import { getPostComments, createComment } from "../../service/commentService";
import type { Post } from "../../types/post";
import type { Comment } from "../../types/comment";

interface TimelinePostProps {
  post: Post;
}

function TimelinePost({ post }: TimelinePostProps) {
  const [showDropdown, setShowDropdown] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [isLiked, setIsLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likes_count);
  const [isToggling, setIsToggling] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [submittingComment, setSubmittingComment] = useState(false);

  useEffect(() => {
    if (post.comments_count > 0) {
      getPostComments(post.id)
        .then((response) => setComments(response.comments || []))
        .catch((error) => console.error("Error fetching comments:", error));
    }
  }, [post.id, post.comments_count]);

  // Utility functions
  const formatTimeAgo = (dateString: string) => {
    const diffInSeconds = Math.floor(
      (Date.now() - new Date(dateString).getTime()) / 1000
    );
    if (diffInSeconds < 60) return "Just now";
    if (diffInSeconds < 3600)
      return `${Math.floor(diffInSeconds / 60)} minute${
        Math.floor(diffInSeconds / 60) > 1 ? "s" : ""
      } ago`;
    if (diffInSeconds < 86400)
      return `${Math.floor(diffInSeconds / 3600)} hour${
        Math.floor(diffInSeconds / 3600) > 1 ? "s" : ""
      } ago`;
    return `${Math.floor(diffInSeconds / 86400)} day${
      Math.floor(diffInSeconds / 86400) > 1 ? "s" : ""
    } ago`;
  };

  const getFullName = (author?: { first_name: string; last_name: string }) => {
    return author ? `${author.first_name} ${author.last_name}` : "Unknown User";
  };

  const getImageUrl = (url: string | null | undefined) => {
    if (!url) return null;
    if (url.startsWith("/uploads")) {
      const baseURL = (
        import.meta.env.VITE_API_URL || "http://localhost:8000/api"
      ).replace("/api", "");
      return `${baseURL}${url}`;
    }
    return url;
  };

  const handleLikeToggle = async () => {
    if (isToggling) return;
    try {
      setIsToggling(true);
      const response = await togglePostLike(post.id);
      setIsLiked(response.is_liked);
      setLikesCount(response.total_likes);
    } catch (error) {
      console.error("Error toggling like:", error);
    } finally {
      setIsToggling(false);
    }
  };

  const handleSubmitComment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim() || submittingComment) return;

    try {
      setSubmittingComment(true);
      const newComment = await createComment(post.id, commentText.trim());
      setComments((prev) => [newComment, ...prev]);
      setCommentText("");
    } catch (error: any) {
      console.error("Error creating comment:", error);
      alert(
        error?.response?.data?.detail ||
          error?.message ||
          "Failed to create comment."
      );
    } finally {
      setSubmittingComment(false);
    }
  };

  const postImageUrl = getImageUrl(post.image_url);

  return (
    <div className="_feed_inner_timeline_post_area _b_radious6 _padd_b24 _padd_t24 _mar_b16">
      <div className="_feed_inner_timeline_content _padd_r24 _padd_l24">
        <div className="_feed_inner_timeline_post_top">
          <div className="_feed_inner_timeline_post_box">
            <div className="_feed_inner_timeline_post_box_image">
              {post.author?.avatar_url && (
                <img
                  src={post.author?.avatar_url}
                  alt={getFullName(post.author)}
                  className="_post_img"
                />
              )}
            </div>
            <div className="_feed_inner_timeline_post_box_txt">
              <h4 className="_feed_inner_timeline_post_box_title">
                {getFullName(post.author)}
              </h4>
              <p className="_feed_inner_timeline_post_box_para">
                {formatTimeAgo(post.created_at)} .{" "}
                <a href="#0">
                  {post.visibility === "public" ? "Public" : "Private"}
                </a>
              </p>
            </div>
          </div>
          <div className="_feed_inner_timeline_post_box_dropdown">
            <button
              className="_feed_timeline_post_dropdown_link"
              onClick={() => setShowDropdown(!showDropdown)}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="4"
                height="17"
                fill="none"
                viewBox="0 0 4 17"
              >
                <circle cx="2" cy="2" r="2" fill="#C4C4C4" />
                <circle cx="2" cy="8" r="2" fill="#C4C4C4" />
                <circle cx="2" cy="15" r="2" fill="#C4C4C4" />
              </svg>
            </button>
            {showDropdown && (
              <div className="_feed_timeline_dropdown _timeline_dropdown show">
                <ul className="_feed_timeline_dropdown_list">
                  <li className="_feed_timeline_dropdown_item">
                    <a href="#0" className="_feed_timeline_dropdown_link">
                      Save Post
                    </a>
                  </li>
                  <li className="_feed_timeline_dropdown_item">
                    <a href="#0" className="_feed_timeline_dropdown_link">
                      Edit Post
                    </a>
                  </li>
                  <li className="_feed_timeline_dropdown_item">
                    <a href="#0" className="_feed_timeline_dropdown_link">
                      Delete Post
                    </a>
                  </li>
                </ul>
              </div>
            )}
          </div>
        </div>
        <h4 className="_feed_inner_timeline_post_title">{post.content}</h4>
        {postImageUrl && (
          <div className="_feed_inner_timeline_image">
            <img src={postImageUrl} alt="Post" className="_time_img" />
          </div>
        )}
      </div>

      <div className="_feed_inner_timeline_total_reacts _padd_r24 _padd_l24 _mar_b26">
        <div className="_feed_inner_timeline_total_reacts_image">
          <p className="_feed_inner_timeline_total_reacts_para">
            {likesCount}+
          </p>
        </div>
        <div className="_feed_inner_timeline_total_reacts_txt">
          <p className="_feed_inner_timeline_total_reacts_para1">
            <a href="#0">
              <span>{post.comments_count}</span> Comment
            </a>
          </p>
        </div>
      </div>

      <div className="_feed_inner_timeline_reaction">
        <button
          className={`_feed_inner_timeline_reaction_emoji _feed_reaction ${
            isLiked ? "_feed_reaction_active" : ""
          }`}
          onClick={handleLikeToggle}
          disabled={isToggling}
        >
          <span className="_feed_inner_timeline_reaction_link">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="19"
              height="19"
              fill="currentColor"
              viewBox="0 0 24 24"
              style={{ color: isLiked ? "#e91e63" : "#666" }}
            >
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            Love
          </span>
        </button>
      </div>

      <div className="_feed_inner_timeline_cooment_area">
        <div className="_feed_inner_comment_box">
          <form
            className="_feed_inner_comment_box_form"
            onSubmit={handleSubmitComment}
          >
            <div className="_feed_inner_comment_box_content">
              <div className="_feed_inner_comment_box_content_image">
                <img
                  src="/assets/images/comment_img.png"
                  alt=""
                  className="_comment_img"
                />
              </div>
              <div className="_feed_inner_comment_box_content_txt">
                <textarea
                  className="form-control _comment_textarea"
                  placeholder="Write a comment"
                  value={commentText}
                  onChange={(e) => setCommentText(e.target.value)}
                />
              </div>
            </div>
            <div
              style={{
                marginTop: "8px",
                display: "flex",
                justifyContent: "flex-end",
              }}
            >
              <button
                type="submit"
                disabled={submittingComment || !commentText.trim()}
                style={{
                  padding: "6px 16px",
                  backgroundColor: commentText.trim() ? "#1890FF" : "#ccc",
                  color: "#fff",
                  border: "none",
                  borderRadius: "4px",
                  cursor: commentText.trim() ? "pointer" : "not-allowed",
                  fontSize: "14px",
                  fontWeight: "500",
                }}
              >
                {submittingComment ? "Sending..." : "Send"}
              </button>
            </div>
          </form>
        </div>
      </div>

      {comments.length > 0 && (
        <div className="_timline_comment_main">
          {comments.length > 3 && (
            <div className="_previous_comment">
              <button type="button" className="_previous_comment_txt">
                View {comments.length - 3} previous comments
              </button>
            </div>
          )}
          {comments.slice(0, 3).map((comment) => (
            <div key={comment.id} className="_comment_main">
              <div className="_comment_image">
                <Link to="/profile" className="_comment_image_link">
                  <img
                    src={comment.author?.avatar_url}
                    alt={getFullName(comment.author)}
                    className="_comment_img1"
                  />
                </Link>
              </div>
              <div className="_comment_area">
                <div className="_comment_details">
                  <div className="_comment_details_top">
                    <div className="_comment_name">
                      <Link to="/profile">
                        <h4 className="_comment_name_title">
                          {getFullName(comment.author)}
                        </h4>
                      </Link>
                    </div>
                  </div>
                  <div className="_comment_status">
                    <p className="_comment_status_text">
                      <span>{comment.content}</span>
                    </p>
                  </div>
                  <div className="_total_reactions">
                    <span className="_total">{comment.likes_count}</span>
                  </div>
                  <div className="_comment_reply">
                    <div className="_comment_reply_num">
                      <ul className="_comment_reply_list">
                        <li>
                          <span>Like.</span>
                        </li>
                        <li>
                          <span>Reply.</span>
                        </li>
                        <li>
                          <span className="_time_link">
                            {formatTimeAgo(comment.created_at)}
                          </span>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default TimelinePost;
