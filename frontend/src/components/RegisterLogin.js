import React, { useState } from "react";
import { TextField, Button, Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";


const RegisterLogin = () => {
  const [username, setUsername] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    const trimmedUsername = username.trim();

    try {
      const response = await fetch("http://localhost:5000/add_new_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_name: trimmedUsername }),
      });

      if (response.ok) {
        const data = await response.json();
        const questionObj = data.question;

        localStorage.setItem("user_id", data.player_id);
        localStorage.setItem("game_id", data.game_id);
        localStorage.setItem("question_id", data.question.question_id);

        navigate("/game", { state: { questionObj } });
      } else if (response.status === 400) {
        const errorData = await response.json();
        alert(errorData.message);
      } else {
        alert("An error occurred. Please try again later.");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      alert("An unexpected error occurred. Please try again later.");
    }
  };

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
        sx={{ fontFamily: "Ultra" }}
        color="primary"
      >
        Enter your name
      </Typography>
      <TextField
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <Button variant="outlined" onClick={handleLogin}>
        START QUIZ
      </Button>
    </Box>
  );
};

export default RegisterLogin;
