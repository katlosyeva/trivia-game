// RegisterLogin.js
import React, { useState } from "react";
import { TextField, Button, Box } from "@mui/material";

const RegisterLogin = ({ onLogin }) => {
  const [username, setUsername] = useState("");
  console.log(
    "🚀 ~ file: RegisterLogin.js:7 ~ RegisterLogin ~ username:",
    username
  );
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    // Send login data to the backend
    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Save user_id and game_id to localStorage
        localStorage.setItem("user_id", data.user_id);
        localStorage.setItem("game_id", data.game_id);

        // Trigger the onLogin callback
        onLogin();
      })
      .catch((error) => console.error("Error logging in:", error));
  };

  return (
    <Box sx={{ m: 4 }}>
      <TextField
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button variant="contained" color="primary" onClick={handleLogin}>
        Login
      </Button>
    </Box>
  );
};

export default RegisterLogin;
