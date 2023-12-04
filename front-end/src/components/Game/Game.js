import React, { useState } from "react";
import { Box, Button, Typography } from "@mui/material";
import Question from "./Question";
import { useLocation, useNavigate } from "react-router-dom";
import backgroundImage from "../../assets/background2.jpg";

const shuffleArray = (array) => {
  const shuffledArray = [...array];
  for (let i = shuffledArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
};

const Game = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const questionObj = location.state.questionObj;

  const [answers, setAnswers] = useState(questionObj.answers);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [correctAnswer, setCorrectAnswer] = useState("");
  const [showCorrectAnswer, setShowCorrectAnswer] = useState(false);
  const [questionsCount, setQuestionsCount] = useState(1);
  const [question, setQuestion] = useState(questionObj.question_text);
  const [remainingHints, setRemainingHints] = useState(3);

  const game_id = Number(localStorage.getItem("game_id"));

  const fetchQuestions = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/next_question/${game_id}`
      );
      const data = await response.json();

      if (data) {
        localStorage.setItem("question_id", data.question_id);
        setQuestion(data.question_text);
        setAnswers(shuffleArray(data.answers));
        setSelectedAnswer(null);
        setShowCorrectAnswer(false);
      }
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
  };

  const handleAnswerChange = (event) => {
    setSelectedAnswer(event.target.value);
  };

  const handleSubmit = async () => {
    const question_id = localStorage.getItem("question_id");
    try {
      const response = await fetch("http://127.0.0.1:5000/check_answer", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          game_id: game_id,
          answer: selectedAnswer,
          question_id: question_id,
        }),
      });

      const result = await response.json();
      setCorrectAnswer(result.correct_answer);
      setScore(result.score);
      setShowCorrectAnswer(true);
    } catch (error) {
      console.error("Error submitting answer:", error);
    }
  };

  const handleHint = async () => {
    if (remainingHints > 0) {
      const question_id = localStorage.getItem("question_id");
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/fifty_fifty/${question_id}`
        );
        const data = await response.json();

        if (data) {
          setAnswers(data.answers);
          setSelectedAnswer(null);
          setShowCorrectAnswer(false);
          setRemainingHints((prevHints) => prevHints - 1); // Decrement remaining hints
        }
      } catch (error) {
        console.error("Error submitting answer:", error);
      }
    }
  };

  const handleNext = async () => {
    setQuestionsCount(questionsCount + 1);
    if (questionsCount >= 15) {
      navigate("/congratulations", { state: { score } });
    } else {
      fetchQuestions();
    }
  };

  return (
    <Box
      sx={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundRepeat: false,
        backgroundPosition: "center",
        backgroundSize: "200%",
        display: "flex",
        alignItems: "center",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <Box
        sx={{
          display: "flex",
          flex: "1",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          m: "0 auto",
          gap: 3,
        }}
      >
        <Typography variant="h4">Question {questionsCount}</Typography>
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
          {" "}
          <Button
            variant="contained"
            color="primary"
            onClick={handleHint}
            disabled={showCorrectAnswer || remainingHints === 0}
          >
            Hint ({remainingHints} left)
          </Button>
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
        <Typography variant="h6">Score: {score}</Typography>
      </Box>
      {showCorrectAnswer && (
        <Box
          sx={{
            minHeight: 100,
            m: "0 auto",
            gap: 3,
            position: "absolute",
            bottom: 100,
          }}
        >
          <Typography variant="h6" sx={{ color: "green" }}>
            Correct Answer: {correctAnswer}
          </Typography>
          {selectedAnswer !== correctAnswer && (
            <Typography variant="h6" sx={{ color: "red" }}>
              Your Answer: {selectedAnswer}
            </Typography>
          )}
        </Box>
      )}
    </Box>
  );
};

export default Game;
