import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';

function SingleBlog() {
  const location = useLocation();
  const data = location.state?.data || [];
  
  const [likes, setLikes] = useState(0);

  const handleLike = () => {
    setLikes(likes + 1);
  };

  return (
    <>
      <div className="container mt-5 mb-3 ht-100">
        <div className="row justify-content-center">
          <div className="col-md-12">
            <div
              className="card"
              style={{ marginTop: "56px", marginBottom: "3rem" }}
            >
              <div className="card-body">
                <h5 className="card-title">{data.blog_title}</h5>
                <p>
                  {data.blog_content}
                </p>
                <p className="card-text">
                  <b>Author: </b>
                  {data.user_id}
                </p>
                <button onClick={handleLike} className="btn btn-primary">
                  Like {likes}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SingleBlog;
