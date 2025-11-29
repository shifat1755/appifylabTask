import { useEffect } from "react";
import Header from "../components/feed/Header";
import MiddleFeed from "../components/feed/MiddleFeed";
import { useAuthContext } from "../context/AuthContext";
import { userInfo } from "../service/userService";

function Feed() {
  const { setUser } = useAuthContext();

  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
    try {
      const response = await userInfo();
      setUser(response);
    } catch (err) {
      throw err;
    }
  };

  return (
    <div className="_main_layout">
      <Header />

      {/* Main Layout Structure */}
      <div className="container _custom_container">
        <div className="_layout_inner_wrap">
          <div className="row justify-content-center">
            <MiddleFeed />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Feed;
