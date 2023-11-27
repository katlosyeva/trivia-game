import React from "react";
import { FormControlLabel, Radio, RadioGroup, Typography } from "@mui/material";

const Question = ({
  question,
  answers,
  selectedAnswer,
  onChange,
  disabled,
}) => {
  const sanitizedQuestion = question
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&aacute;/g, "á");
  const sanitizedAnswers = answers.map((answer) =>
    answer
      .replace(/&quot;/g, '"')
      .replace(/&#039;/g, "'")
      .replace(/&aacute;/g, "á")
  );

  return (
    <div>
      <Typography variant="h5" sx={{ maxWidth: 500, mb: 2 }}>
        {sanitizedQuestion}
      </Typography>
      <RadioGroup
        aria-label="answers"
        name="answers"
        value={selectedAnswer}
        onChange={onChange}
        disabled={disabled}
        sx={{
          height: 90,
          display: "flex",
          flexDirection: "column",
          flexWrap: true,
        }}
      >
        {sanitizedAnswers.map((answer, index) => (
          <FormControlLabel
            key={index}
            value={answer}
            control={<Radio />}
            label={answer}
            disabled={disabled}
          />
        ))}
      </RadioGroup>
    </div>
  );
};

export default Question;
