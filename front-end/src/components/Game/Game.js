import React, { useState } from "react";
import { Box, Button, Typography } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';
import Question from "./Question";
import { useLocation, useNavigate } from "react-router-dom";
import backgroundImage from "../../assets/background2.jpg";
import 'chart.js/auto';
import { Pie } from "react-chartjs-2";
import Modal from 'react-modal';

const shuffleArray = (array) => {
  const shuffledArray = [...array];
  for (let i = shuffledArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
};

// const customStyles = {
//   content: {
//     top: '50%',
//     left: '50%',
//     right: 'auto',
//     bottom: 'auto',
//     marginRight: '-50%',
//     transform: 'translate(-50%, -50%)',
//   },
// };
const customStyles = {
  content: {
    top: '20%',
    left: 'auto',
    right: '5%',
    bottom: 'auto',
    // marginRight: '-50%',
    // transform: 'translate(-50%, -50%)',
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
  const [remainingHints, setRemainingHints] = useState(3);
  const [audienceChoice, setAudienceChoice] = useState("");
  const [modalIsOpen, setModalIsOpen] = useState(false);
  console.log(audienceChoice)

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
  
  const handleAskAudience = async() => {
    if (remainingHints > 0) {
      const question_id = localStorage.getItem("question_id");
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/ask_audience/${question_id}`
        );
        const data = await response.json();
        console.log("data", data)
        if (data) {
          setAudienceChoice(data)
          setRemainingHints((prevHints) => prevHints - 1); // Decrement remaining hints
          
        }
      } catch (error) {
        console.error("Error submitting answer:", error);
      }
    }
  }

  const openModal = () => {
    handleAskAudience()
    console.log("From", audienceChoice)
    setModalIsOpen(true);
  };
  
  

  // const openModal = () => {
  //   setModalIsOpen(true);
  // };

  const closeModal = () => {
    setModalIsOpen(false);
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
          {/* <Button
            variant="contained"
            color="primary"
            onClick={handleHint}
            disabled={showCorrectAnswer || remainingHints === 0}
          >
            Ask audience ({remainingHints} left)
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleHint}
            disabled={showCorrectAnswer || remainingHints === 0}
          >
            Try 50/50 ({remainingHints} left)
          </Button> */}
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
            onClick={openModal}
            disabled={showCorrectAnswer || remainingHints === 0}
          >
            Ask audience ({remainingHints} left)
          </Button>
          <Button
            variant="contained"
            color="primary"
            onClick={handleHint}
            disabled={showCorrectAnswer || remainingHints === 0}
          >
            Try 50/50 ({remainingHints} left)
          </Button>
          {/* <Button
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
          </Button> */}
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
      {audienceChoice &&
      <Modal
        style={customStyles}
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Example Modal"
      >
        <CloseIcon onClick={closeModal} color="primary"/>
        <Pie style={{"font":"20px"}}
          options = {{
            plugins: {
              legend: {
                labels: {
                  font: {
                    family: 'Arial', 
                    size: 20,        
                  },
                },
              },
            },
          }}
          data={{
          labels: [audienceChoice[0][1], audienceChoice[1][1], audienceChoice[2][1], audienceChoice[3][1]],
          datasets: [
          {
            label: '%',
            data: [audienceChoice[0][0], audienceChoice[1][0], audienceChoice[2][0], audienceChoice[3][0]],
          },
        ],
      
      }}
      
      height={400}
      width={400}
    />
    
    </Modal>
    }
    {/* <Typography style={{"position":"absolute", "top":"10px", "right":"10px"}}>Score</Typography> */}
    </Box>
    
  );
};

export default Game;
