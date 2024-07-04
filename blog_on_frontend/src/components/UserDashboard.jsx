import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, ListGroup } from "react-bootstrap";

function UserDashboard() {
  const [user, setUser] = useState(null);
  const fetchUserInfo = async (user_id) => {
    try {
      const response = await fetch(`http://localhost:8000/users/${user_id}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setUser(data);
      // console.log(data);
    } catch (error) {
      console.error("Fetch error:", error);
    }
  };
  useEffect(() => {
    fetchUserInfo(1);
  }, []);
  console.log(user);
  return (
    <Container className="mt-5">
      <Row>
        <Col>
          <Card>
            <Card.Header as="h2">User Dashboard</Card.Header>
            <Card.Body>
              {user ? (
                <>
                  <Card.Title>{user.username}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">
                    {user.email_id}
                  </Card.Subtitle>
                  <Card.Text>Here are the blogs written by you:</Card.Text>
                  {/* <ListGroup variant="flush">
                    {user.blogs.map((blog, index) => (
                      <ListGroup.Item key={index}>{blog}</ListGroup.Item>
                    ))}
                  </ListGroup> */}
                </>
              ) : (
                <Card.Text>Loading...</Card.Text>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default UserDashboard;
