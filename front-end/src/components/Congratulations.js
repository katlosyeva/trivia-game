import React from "react";
import { Typography, Button, Box } from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import backgroundImage from "../assets/background2.jpg";

const Congratulations = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const score = location.state.score;

  const handlePlayAgain = () => {
    navigate("/");
  };

  return (
    <Box
      sx={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundPosition: "center",
        backgroundSize: "200%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        minHeight: "100vh",
        m: "0 auto",
        gap: 3,
      }}
    >
      <Typography variant="h4" gutterBottom>
        Congratulations!
      </Typography>
      <Typography variant="h6" paragraph>
        You scored {score} points.
      </Typography>
      <Button variant="contained" color="primary" onClick={handlePlayAgain}>
        Play Again
      </Button>
    </Box>
  );
};

export default Congratulations;
