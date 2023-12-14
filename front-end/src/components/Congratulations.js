import React from "react";
import { Typography, Button, Box } from "@mui/material";
import { Link, useLocation } from "react-router-dom";

const Congratulations = () => {
  const location = useLocation();
  const score = location.state.score;

  return (
    <Box
      sx={{
        backgroundColor: "#d9ecf3",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        minHeight: "100vh",
        m: "0 auto",
        gap: 3,
      }}
    >
      <Typography
        variant="h4"
        gutterBottom
        color="primary"
        sx={{ fontFamily: "Ultra" }}
      >
        Congratulations!
      </Typography>
      <Typography variant="h6" paragraph>
        You scored {score} points.
      </Typography>
      <Button variant="outlined" component={Link} to="/">
        Play Again
      </Button>
      <Button component={Link} to="/leaderboard" variant="outlined">
        Leaderboard 🏆
      </Button>
    </Box>
  );
};

export default Congratulations;
