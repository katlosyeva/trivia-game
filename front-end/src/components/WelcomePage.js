import React from "react";
import { Link } from "react-router-dom";
import { Box, Button, Typography } from "@mui/material";

const WelcomePage = () => {
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
        gap: 2,
      }}
    >
      <Typography variant="h4" gutterBottom>
        Welcome to Trivia Game
      </Typography>
      <Typography variant="body1" paragraph>
        To start the game, please login.
      </Typography>
      <Button component={Link} to="/login" variant="contained" color="primary">
        Login
      </Button>
    </Box>
  );
};

export default WelcomePage;
