import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import Question from "./Question";
import { useLocation, useNavigate } from "react-router-dom";
import "chart.js/auto";
import { Pie } from "react-chartjs-2";
import Modal from "react-modal";

const customStyles = {
  content: {
    top: "20%",
    left: "auto",
    right: "5%",
    bottom: "auto",
  },
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
  const [hintUsed, setHintUsed] = useState(false);
  const [remaining50_50Hints, setRemaining50_50Hints] = useState(2);
  const [remainingAskAudienceHints, setRemainingAskAudienceHints] = useState(2);
  const [audienceChoice, setAudienceChoice] = useState("");
  const [modalIsOpen, setModalIsOpen] = useState(false);

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
        setAnswers(data.answers);
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

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      setCorrectAnswer(result.correct_answer);
      setScore(result.score);
      setShowCorrectAnswer(true);
    } catch (error) {
      console.error("Error submitting answer:", error.message);
    }
  };

  const handleHint = async () => {
    if (remaining50_50Hints > 0 && !hintUsed) {
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
          setRemaining50_50Hints((prevHints) => prevHints - 1);
          setHintUsed(true);
        }
      } catch (error) {
        console.error("Error submitting answer:", error);
      }
    }
  };

  const handleAskAudience = async () => {
    if (remainingAskAudienceHints > 0 && !hintUsed) {
      const question_id = localStorage.getItem("question_id");
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/ask_audience/${question_id}`
        );
        const data = await response.json();
        if (data) {
          setAudienceChoice(data);
          setRemainingAskAudienceHints((prevHints) => prevHints - 1);
          setHintUsed(true);
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
      setHintUsed(false);
      fetchQuestions();
    }
  };

  const openModal = () => {
    handleAskAudience();
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <Box
      sx={{
        backgroundColor: "#d9ecf3",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexDirection: "column",
        minHeight: "100vh",
      }}
    >
      <Card sx={{ width: 700 }}>
        <CardContent>
          <Typography variant="h4" color="primary" gutterBottom>
            Question {questionsCount}
          </Typography>
          <Question
            question={question}
            answers={answers}
            selectedAnswer={selectedAnswer}
            onChange={handleAnswerChange}
            disabled={showCorrectAnswer}
          />
        </CardContent>
        <CardActions>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={!selectedAnswer || showCorrectAnswer}
          >
            Submit
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            disabled={!showCorrectAnswer}
          >
            Next
          </Button>
        </CardActions>
      </Card>
      <Box
        sx={{
          display: "flex",
          gap: 2,
          position: "absolute",
          top: 20,
          right: 20,
        }}
      >
        <Button
          variant="outlined"
          onClick={openModal}
          disabled={
            showCorrectAnswer || remainingAskAudienceHints === 0 || hintUsed
          }
          sx={{ fontWeight: "bold" }}
        >
          Ask audience ({remainingAskAudienceHints} left)
        </Button>
        <Button
          variant="outlined"
          onClick={handleHint}
          sx={{ fontWeight: "bold" }}
          disabled={showCorrectAnswer || remaining50_50Hints === 0 || hintUsed}
        >
          Try 50/50 ({remaining50_50Hints} left)
        </Button>
      </Box>
      {showCorrectAnswer && (
        <Box
          sx={{
            minHeight: 100,
            m: "0 auto",
            gap: 3,
            position: "absolute",
            bottom: 90,
          }}
        >
          <Typography variant="h6" color="darkGreen">
            Correct Answer: {correctAnswer}
          </Typography>
          {selectedAnswer !== correctAnswer && (
            <Typography variant="h6" color="error">
              Your Answer: {selectedAnswer}
            </Typography>
          )}
        </Box>
      )}
      <Typography
        variant="h5"
        sx={{ position: "absolute", bottom: 30, right: 30 }}
      >
        Score: {score}
      </Typography>
      {audienceChoice && (
        <Modal
          style={customStyles}
          isOpen={modalIsOpen}
          onRequestClose={closeModal}
          contentLabel="Example Modal"
        >
          <CloseIcon onClick={closeModal} color="primary" />
          <Pie
            style={{ font: "20px" }}
            options={{
              plugins: {
                legend: {
                  labels: {
                    font: {
                      family: "Arial",
                      size: 20,
                    },
                  },
                },
              },
            }}
            data={{
              labels: [
                audienceChoice[0][1],
                audienceChoice[1][1],
                audienceChoice[2][1],
                audienceChoice[3][1],
              ],
              datasets: [
                {
                  label: "%",
                  data: [
                    audienceChoice[0][0],
                    audienceChoice[1][0],
                    audienceChoice[2][0],
                    audienceChoice[3][0],
                  ],
                },
              ],
            }}
            height={400}
            width={400}
          />
        </Modal>
      )}
    </Box>
  );
};

export default Game;
