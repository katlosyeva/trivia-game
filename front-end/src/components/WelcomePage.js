// WelcomePage.js
import React from "react";
import { Link } from "react-router-dom";
import { Button, Typography } from "@mui/material";

const WelcomePage = () => {
  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Welcome to Trivia Game
      </Typography>
      <Typography variant="body1" paragraph>
        To start the game, please login.
      </Typography>
      <Button
        component={Link}
        to="/login"
        variant="contained"
        color="primary"
        style={{ marginLeft: "10px" }}
      >
        Login
      </Button>
    </div>
  );
};

export default WelcomePage;
