import React, { useState } from 'react';

function AddBlog() {
  const [formState, setFormState] = useState({
    user_id: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormState({
      ...formState,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { ...formState };
    data["user_id"] = Number(data["user_id"]);
    data["likes"] = null;
    console.log(data);
    try {
      const response = await fetch('http://localhost:8000/add_blog', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      console.log(response);
      if (response.ok) {
        const result = await response.json();
        console.log('Blog added successfully:', result);
      } else {
        console.error('Error adding blog:', response.statusText);
      }
    } catch (error) {
      console.error('Error adding blog:', error);
    }
  };

return (
    <>
     <div className="container mt-5">
      <form onSubmit={handleSubmit}>
        <center>
          <h1>Add Blog</h1>
        </center>
        {/* <div className="mb-3">
          <label htmlFor="user_id" className="form-label">
            User ID
          </label>
          <input
            type="text"
            id="user_id"
            name="user_id"
            className="form-control"
            placeholder="User ID"
            value={formState.user_id}
            onChange={handleInputChange}
          />
        </div> */}
        <div className="mb-3">
          <label htmlFor="exampleInputEmail1" className="form-label">
            <b>Blog Title</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleInputTitle"
            aria-describedby="emailHelp"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="exampleInputPassword1" className="form-label">
            <b>Blog Summary</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleInputDescription"
          />
        </div>
        <div className="mb-3">
          <label htmlFor="exampleInputPassword1" className="form-label">
            <b>Blog Content</b>
          </label>
          <input
            type="text"
            className="form-control"
            id="exampleInputDescription"
          />
        </div>
        <center>
          <button type="submit" className="btn btn-primary">
            Submit
          </button>
        </center>
      </form>
    </div>
    </>
  );
}
export default AddBlog;
