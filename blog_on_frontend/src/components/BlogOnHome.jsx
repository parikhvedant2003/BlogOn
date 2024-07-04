import React, {useState, useEffect} from "react";
import ReactDOM from "react-dom/client";
import { Link } from "react-router-dom";

function BlogOnHome() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/blogs')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error:', error));
  }, []);
  return (
    <>
      <div className="container-fluid m-0 p-0 mt-4 mb-4">
        <div className="d-flex flex-wrap" style={{width: "100%", gap:"3.33%",justifyContent: "space-between"}}>
          {(data?data:[]).map((item, index) => (
            <div
              key={index}
              className="flex-grow-1 mb-4"
              style={{
                flexBasis: "30%",
              }}
            >
              <div className="card" style={{ width: "100%" }}>
                <div className="card-body">
                  <h5 className="card-title"><b>{item.blog_title}</b></h5>
                  <p className="card-text">
                    {item.blog_summary}
                  </p>
                  <p><b>Author: </b>{item.user_id}</p>
                  <Link to={`/blog/${data[index].blog_id}`} state={{data: data[index]}} className="btn btn-primary">
                    Open
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
export default BlogOnHome;
