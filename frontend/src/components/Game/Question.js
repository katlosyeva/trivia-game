import React from "react";
import { FormControlLabel, Radio, RadioGroup, Typography } from "@mui/material";

const Question = ({
  question,
  answers,
  selectedAnswer,
  onChange,
  disabled,
}) => {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        {question}
      </Typography>

      <RadioGroup
        aria-label="answers"
        name="answers"
        value={selectedAnswer}
        onChange={onChange}
        disabled={disabled}
        sx={{
          display: "flex",
          flexDirection: "column",
          flexWrap: "wrap",
        }}
      >
        {answers.map((answer, index) => (
          <FormControlLabel
            key={index}
            value={answer}
            control={<Radio />}
            label={answer}
            disabled={disabled}
          />
        ))}
      </RadioGroup>
    </>
  );
};

export default Question;
