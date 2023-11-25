import React, { useState, useEffect } from "react";
import { Box, Button, Typography } from "@mui/material";
import Question from "./Question";
import { useLocation, useNavigate } from "react-router-dom";

const Game = () => {
  const [answers, setAnswers] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [correctAnswer, setCorrectAnswer] = useState(null);
  const [showCorrectAnswer, setShowCorrectAnswer] = useState(false);
  const [questionsCount, setQuestionsCount] = useState(1);
  const location = useLocation();
  const question = location.state;
  const navigate = useNavigate();
  const game_id = localStorage.getItem("game_id");

  const shuffleArray = (array) => {
    const shuffledArray = [...array];
    for (let i = shuffledArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffledArray[i], shuffledArray[j]] = [
        shuffledArray[j],
        shuffledArray[i],
      ];
    }
    return shuffledArray;
  };

  // const fetchQuestions = async () => {
  //   try {
  //     const response = await fetch(
  //       `http://127.0.0.1:5000/next_question/${game_id}`
  //     );
  //     const data = await response.json();

  //     if (data.question) {
  //       const { question, answers } = data;
  //       setQuestion(question);
  //       setAnswers(shuffleArray(answers));
  //       setSelectedAnswer(null);
  //       setShowCorrectAnswer(false);
  //     }
  //   } catch (error) {
  //     console.error("Error fetching questions:", error);
  //   }
  // };

  // useEffect(() => {
  //   fetchQuestions();
  // }, []);

  const handleAnswerChange = (event) => {
    setSelectedAnswer(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/check_answer", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          game_id: game_id,
          answer: selectedAnswer,
          question_id: 1, // You need to get the question_id from the API response
        }),
      });
      const result = await response.json();
      setCorrectAnswer(result.correctAnswer);

      if (result.correct) {
        setScore(score + 1);
      }

      setShowCorrectAnswer(true);
    } catch (error) {
      console.error("Error submitting answer:", error);
    }
  };

  const handleNext = async () => {
    setQuestionsCount(questionsCount + 1);
    if (questionsCount >= 5) {
      navigate("/congratulations", { state: { score } });
    }
  };

  return (
    <Box
      sx={{
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
        Question {questionsCount}
      </Typography>
      {/* Assume Question component receives props correctly */}
      <Question
        question={question}
        answers={answers}
        selectedAnswer={selectedAnswer}
        onChange={handleAnswerChange}
        disabled={showCorrectAnswer}
      />
      <Box
        sx={{
          display: "flex",
          gap: 2,
        }}
      >
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={!selectedAnswer || showCorrectAnswer}
        >
          Submit
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleNext}
          disabled={!showCorrectAnswer}
        >
          Next
        </Button>
      </Box>
      {showCorrectAnswer && (
        <Box>
          <Typography variant="h6" style={{ color: "green" }}>
            Correct Answer: {correctAnswer}
          </Typography>
          {selectedAnswer !== correctAnswer && (
            <Typography variant="h6" style={{ color: "red" }}>
              Your Answer: {selectedAnswer}
            </Typography>
          )}
        </Box>
      )}
      <Typography variant="h6">Score: {score}</Typography>
    </Box>
  );
};

export default Game;
