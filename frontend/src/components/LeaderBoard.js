import React, { useEffect, useState } from "react";
import {
  Typography,
  Table,
  TableContainer,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Box,
  Button,
} from "@mui/material";
import { Link } from "react-router-dom";


const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const response = await fetch("http://localhost:5000/leaderboard");
        const data = await response.json();
        setLeaderboard(data);
      } catch (error) {
        console.error("Error fetching leaderboard:", error);
      }
    };

    fetchLeaderboard();
  }, []);

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
      <Typography variant="h4" color="primary" sx={{ fontFamily: "Ultra" }}>
        Leaderboard 🏆
      </Typography>
      <TableContainer component={Paper} sx={{ maxWidth: 500 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Player</TableCell>
              <TableCell>Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {leaderboard.map((entry, index) => (
              <TableRow key={index}>
                <TableCell sx={{ p: 1, pl: 2 }}>{entry[0]}</TableCell>
                <TableCell sx={{ p: 1, pl: 2 }}>{entry[1]}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <Button variant="outlined" component={Link} to="/">
        Play New Game
      </Button>
    </Box>
  );
};

export default Leaderboard;
