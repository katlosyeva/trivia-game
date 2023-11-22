import React, { useState, useEffect } from "react";
import { Box, Button, Typography } from "@mui/material";
import Question from "./Question";
import { useNavigate } from "react-router-dom";

const Game = () => {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState([]);
  const [correctAnswer, setCorrectAnswer] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [score, setScore] = useState(0);
  const [showCorrectAnswer, setShowCorrectAnswer] = useState(false);
  const [questionsCount, setQuestionsCount] = useState(1);

  const navigate = useNavigate();

  // const user_id = localStorage.getItem("user_id");
  // const game_id = localStorage.getItem("game_id");

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

  const fetchQuestions = async () => {
    try {
      const response = await fetch("https://opentdb.com/api.php?amount=1");
      const data = await response.json();

      if (data.results && data.results.length > 0) {
        const question = data.results[0].question;
        const correct = data.results[0].correct_answer;

        const answers = [correct, ...data.results[0].incorrect_answers];

        const shuffledAnswers = shuffleArray(answers);

        setQuestion(question);
        setAnswers(shuffledAnswers);
        setCorrectAnswer(correct);
        setSelectedAnswer(null);
        setShowCorrectAnswer(false);
      }
    } catch (error) {
      console.error("Error fetching questions:", error);
    }
    // try {
    //   const response = await fetch("http://127.0.0.1:5000/add_new_questions", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       user_id: user_id,
    //       game_id: game_id,
    //     }),
    //   });
    //   console.log(
    //     "🚀 ~ file: Game.js:27 ~ fetchQuestions ~ response:",
    //     response
    //   );

    //   const data = await response.json();

    //   if (data.question) {
    //     const { question, answers } = data;
    //     setQuestion(question);
    //     setAnswers(answers);
    //     setSelectedAnswer(null);
    //     setShowCorrectAnswer(false);
    //   }
    // } catch (error) {
    //   console.error("Error fetching questions:", error);
    // }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  const handleAnswerChange = (event) => {
    setSelectedAnswer(event.target.value);
  };

  const handleSubmit = async () => {
    try {
      if (selectedAnswer === correctAnswer) {
        setScore(score + 1);
      }

      setShowCorrectAnswer(true);
      // const response = await fetch("http://127.0.0.1:5000/check_answer", {
      //   method: "PUT",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify({
      //     user_id: user_id,
      //     game_id: game_id,
      //     user_answer: selectedAnswer,
      //   }),
      // });
      // const result = await response.json();
      // // Assuming the backend sends a field like 'correct' in the result
      // if (result.correct) {
      //   setScore(score + 1);
      // }
    } catch (error) {
      console.error("Error submitting answer:", error);
    }
  };

  const handleNext = async () => {
    fetchQuestions();
    setQuestionsCount(questionsCount + 1);
    if (questionsCount >= 5) {
      navigate("/congratulations", { state: { score } });
    }
    // try {
    //   const response = await fetch(
    //     `http://127.0.0.1:5000/next_question/${game_id}`,
    //     {
    //       method: "GET",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //     }
    //   );

    //   const data = await response.json();

    //   if (data.question) {
    //     const { question, answers } = data;
    //     setQuestion(question);
    //     setAnswers(answers);
    //     setSelectedAnswer(null);
    //     setShowCorrectAnswer(false);
    //   }
    // } catch (error) {
    //   console.error("Error fetching next question:", error);
    // }
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
