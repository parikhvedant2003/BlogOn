import React from "react";
import ReactDOM from "react-dom";
import { Link, Outlet } from "react-router-dom";

function Navbar() {
  return (
    <>
      <nav className="navbar navbar-expand-lg bg-body-tertiary p-0">
        <div className="container-fluid" style={{ backgroundColor: "white" }}>
          <Link className="navbar-brand" to={"/"}>
            <b>BlogOn</b>
          </Link>
          <div className="d-flex justify-content-end align-items-center">
            <Link to={"/add-blog/"}>
              <button className="btn btn-primary">Add Blog</button>
            </Link>
          </div>
          <div className="d-flex justify-content-end align-items-center">
            <Link to={"/sign-in/"}>
              <button className="btn btn-primary">SignIn / SignUp</button>
            </Link>
          </div>
        </div>
      </nav>
      <Outlet />
    </>
  );
}
export default Navbar;
