import React from "react";
function SignIn() {
  return (
    <>
      <div className="container mt-5">
        <form>
          <center>
            <h1>Sign In</h1>
          </center>
          <div class="mb-3">
            <label for="exampleInputEmail1" class="form-label">
              <b>Username</b>
            </label>
            <input
              type="email"
              class="form-control"
              id="exampleInputEmail1"
              aria-describedby="emailHelp"
            />
          </div>
          <div class="mb-3">
            <label for="exampleInputPassword1" class="form-label">
              <b>Password</b>
            </label>
            <input
              type="password"
              class="form-control"
              id="exampleInputPassword1"
            />
          </div>
          <button type="submit" class="btn btn-primary">
            Submit
          </button>
        </form>
      </div>
    </>
  );
}
export default SignIn;
