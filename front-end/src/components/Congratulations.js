// Congratulations.js
import React from "react";
import { Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Congratulations = ({ points }) => {
  const navigate = useNavigate();

  const handlePlayAgain = () => {
    // Navigate to the home page or the starting point of your game
    navigate("/");
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Congratulations!
      </Typography>
      <Typography variant="h6" paragraph>
        You scored {points} points.
      </Typography>
      <Button variant="contained" color="primary" onClick={handlePlayAgain}>
        Play Again
      </Button>
    </div>
  );
};

export default Congratulations;
