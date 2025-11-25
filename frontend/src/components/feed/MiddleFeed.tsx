import { useState, useEffect } from "react";
import PostInput from "./PostInput";
import TimelinePost from "./TimelinePost";
import { getPosts } from "../../service/postService";

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

function MiddleFeed() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const response = await getPosts(0, 20, "newest");
      setPosts(response.posts || []);
      setError(null);
    } catch (err) {
      setError("Failed to load posts");
      console.error("Error fetching posts:", err);
    } finally {
      setLoading(false);
    }
  };

  // Refresh posts after a new post is created
  const handlePostCreated = () => {
    fetchPosts();
  };

  return (
    <div className="col-xl-6 col-lg-6 col-md-12 col-sm-12">
      <div className="_layout_middle_wrap">
        <div className="_layout_middle_inner">
          {/* Stories Section - Desktop */}
          <div className="_feed_inner_ppl_card _mar_b16">
            <div className="_feed_inner_story_arrow">
              <button type="button" className="_feed_inner_story_arrow_btn">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="9"
                  height="8"
                  fill="none"
                  viewBox="0 0 9 8"
                >
                  <path
                    fill="#fff"
                    d="M8 4l.366-.341.318.341-.318.341L8 4zm-7 .5a.5.5 0 010-1v1zM5.566.659l2.8 3-.732.682-2.8-3L5.566.66zm2.8 3.682l-2.8 3-.732-.682 2.8-3 .732.682zM8 4.5H1v-1h7v1z"
                  />
                </svg>
              </button>
            </div>
            <div className="row">
              <div className="col-xl-3 col-lg-3 col-md-4 col-sm-4 col">
                <div className="_feed_inner_profile_story _b_radious6 ">
                  <div className="_feed_inner_profile_story_image">
                    <img
                      src="/assets/images/card_ppl1.png"
                      alt="Image"
                      className="_profile_story_img"
                    />
                    <div className="_feed_inner_story_txt">
                      <div className="_feed_inner_story_btn">
                        <button className="_feed_inner_story_btn_link">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="10"
                            height="10"
                            fill="none"
                            viewBox="0 0 10 10"
                          >
                            <path
                              stroke="#fff"
                              strokeLinecap="round"
                              d="M.5 4.884h9M4.884 9.5v-9"
                            />
                          </svg>
                        </button>
                      </div>
                      <p className="_feed_inner_story_para">Your Story</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-xl-3 col-lg-3 col-md-4 col-sm-4 col">
                <div className="_feed_inner_public_story _b_radious6">
                  <div className="_feed_inner_public_story_image">
                    <img
                      src="/assets/images/card_ppl2.png"
                      alt="Image"
                      className="_public_story_img"
                    />
                    <div className="_feed_inner_pulic_story_txt">
                      <p className="_feed_inner_pulic_story_para">
                        Ryan Roslansky
                      </p>
                    </div>
                    <div className="_feed_inner_public_mini">
                      <img
                        src="/assets/images/mini_pic.png"
                        alt="Image"
                        className="_public_mini_img"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-xl-3 col-lg-3 col-md-4 col-sm-4 _custom_mobile_none">
                <div className="_feed_inner_public_story _b_radious6">
                  <div className="_feed_inner_public_story_image">
                    <img
                      src="/assets/images/card_ppl3.png"
                      alt="Image"
                      className="_public_story_img"
                    />
                    <div className="_feed_inner_pulic_story_txt">
                      <p className="_feed_inner_pulic_story_para">
                        Ryan Roslansky
                      </p>
                    </div>
                    <div className="_feed_inner_public_mini">
                      <img
                        src="/assets/images/mini_pic.png"
                        alt="Image"
                        className="_public_mini_img"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-xl-3 col-lg-3 col-md-4 col-sm-4 _custom_none">
                <div className="_feed_inner_public_story _b_radious6">
                  <div className="_feed_inner_public_story_image">
                    <img
                      src="/assets/images/card_ppl4.png"
                      alt="Image"
                      className="_public_story_img"
                    />
                    <div className="_feed_inner_pulic_story_txt">
                      <p className="_feed_inner_pulic_story_para">
                        Ryan Roslansky
                      </p>
                    </div>
                    <div className="_feed_inner_public_mini">
                      <img
                        src="/assets/images/mini_pic.png"
                        alt="Image"
                        className="_public_mini_img"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Stories Section - Mobile */}
          <div className="_feed_inner_ppl_card_mobile _mar_b16">
            <div className="_feed_inner_ppl_card_area">
              <ul className="_feed_inner_ppl_card_area_list">
                <li className="_feed_inner_ppl_card_area_item">
                  <a href="#0" className="_feed_inner_ppl_card_area_link">
                    <div className="_feed_inner_ppl_card_area_story">
                      <img
                        src="/assets/images/mobile_story_img.png"
                        alt="Image"
                        className="_card_story_img"
                      />
                      <div className="_feed_inner_ppl_btn">
                        <button
                          className="_feed_inner_ppl_btn_link"
                          type="button"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="12"
                            height="12"
                            fill="none"
                            viewBox="0 0 12 12"
                          >
                            <path
                              stroke="#fff"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              d="M6 2.5v7M2.5 6h7"
                            />
                          </svg>
                        </button>
                      </div>
                    </div>
                    <p className="_feed_inner_ppl_card_area_link_txt">
                      Your Story
                    </p>
                  </a>
                </li>
                <li className="_feed_inner_ppl_card_area_item">
                  <a href="#0" className="_feed_inner_ppl_card_area_link">
                    <div className="_feed_inner_ppl_card_area_story_active">
                      <img
                        src="/assets/images/mobile_story_img1.png"
                        alt="Image"
                        className="_card_story_img1"
                      />
                    </div>
                    <p className="_feed_inner_ppl_card_area_txt">Ryan...</p>
                  </a>
                </li>
                <li className="_feed_inner_ppl_card_area_item">
                  <a href="#0" className="_feed_inner_ppl_card_area_link">
                    <div className="_feed_inner_ppl_card_area_story_inactive">
                      <img
                        src="/assets/images/mobile_story_img2.png"
                        alt="Image"
                        className="_card_story_img1"
                      />
                    </div>
                    <p className="_feed_inner_ppl_card_area_txt">Ryan...</p>
                  </a>
                </li>
              </ul>
            </div>
          </div>

          <PostInput onPostCreated={handlePostCreated} />

          {/* Timeline Posts */}
          {loading && (
            <div style={{ textAlign: "center", padding: "20px" }}>
              <p>Loading posts...</p>
            </div>
          )}
          {error && (
            <div style={{ textAlign: "center", padding: "20px", color: "red" }}>
              <p>{error}</p>
            </div>
          )}
          {!loading && !error && posts.length === 0 && (
            <div style={{ textAlign: "center", padding: "20px" }}>
              <p>No posts yet. Be the first to post!</p>
            </div>
          )}
          {!loading &&
            !error &&
            posts.map((post) => <TimelinePost key={post.id} post={post} />)}
        </div>
      </div>
    </div>
  );
}

export default MiddleFeed;
