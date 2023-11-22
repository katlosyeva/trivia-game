import React, { useState, useEffect } from "react";
import { Button, Typography } from "@mui/material";
import Question from "./Question";

const Game = () => {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [showCorrectAnswer, setShowCorrectAnswer] = useState(false);

  const fetchQuestions = async () => {
    try {
      const user_id = localStorage.getItem("user_id");
      const game_id = localStorage.getItem("game_id");

      const response = await fetch("http://127.0.0.1:5000/add_new_questions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: user_id,
          game_id: game_id,
        }),
      });

      const data = await response.json();

      if (data.question) {
        const { question, answers } = data;
        setQuestion(question);
        setAnswers(answers);
        setSelectedAnswer(null);
        setShowCorrectAnswer(false);
      }
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const handleAnswerChange = (event) => {
    setSelectedAnswer(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      const user_id = localStorage.getItem("user_id");
      const game_id = localStorage.getItem("game_id");

      const response = await fetch("http://127.0.0.1:5000/check_answer", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: user_id,
          game_id: game_id,
          user_answer: selectedAnswer,
        }),
      });

      const result = await response.json();

      // Assuming the backend sends a field like 'correct' in the result
      if (result.correct) {
        setScore(score + 1);
      }
    } catch (error) {
      console.error("Error submitting answer:", error);
    }
  };

  const handleNext = async () => {
    try {
      const user_id = localStorage.getItem("user_id");
      const game_id = localStorage.getItem("game_id");

      const response = await fetch(
        `http://127.0.0.1:5000/next_question/${game_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      if (data.question) {
        const { question, answers } = data;
        setQuestion(question);
        setAnswers(answers);
        setSelectedAnswer(null);
        setShowCorrectAnswer(false);
      }
    } catch (error) {
      console.error("Error fetching next question:", error);
    }
  };

  return (
    <div>
      <Question
        question={question}
        answers={answers}
        selectedAnswer={selectedAnswer}
        onChange={handleAnswerChange}
        disabled={showCorrectAnswer}
      />
      <div>
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
      </div>
      {showCorrectAnswer && (
        <div>
          <Typography variant="h6" style={{ color: "green" }}>
            Correct Answer: {answers[0]}
          </Typography>
          {selectedAnswer !== answers[0] && (
            <Typography variant="h6" style={{ color: "red" }}>
              Your Answer: {selectedAnswer}
            </Typography>
          )}
        </div>
      )}
      <Typography variant="h6">Score: {score}</Typography>
    </div>
  );
};

export default Game;
