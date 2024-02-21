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
      <Typography
        variant="h2"
        gutterBottom
        color="primary"
        sx={{ fontFamily: "Ultra" }}
      >
        THE TRIVIA GAME
      </Typography>
      <Button component={Link} to="/login" variant="outlined">
        PLAY
      </Button>
    </Box>
  );
};

export default WelcomePage;
