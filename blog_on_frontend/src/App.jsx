import React from "react";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import BlogOnHome from "./components/BlogOnHome";
import Navbar from "./components/Navbar";
import SingleBlog from "./components/SingleBlog";
import AddBlog from "./components/AddBlog";
import SignIn from "./components/SignIn";
import UserDashboard from "./components/UserDashboard";
export default function App() {
  return (
    <>
      <main style={{ fontFamily: "Papyrus" }}>
        <Router>
          <Routes>
            <Route path="/" element={<Navbar />}>
              <Route index element={<UserDashboard />} />
              <Route path="/sign-in/" element={<SignIn />} />
              <Route path="/add-blog/" element={<AddBlog />} />
              <Route path="/blog/:id" element={<SingleBlog />} />
            </Route>
          </Routes>
        </Router>
      </main>
    </>
  );
}
