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
    <div>
      <Typography
        variant="h5"
        sx={{ maxWidth: 500, mb: 2 }}
        dangerouslySetInnerHTML={{ __html: question }}
      />

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
        {answers.map((answer, index) => (
          <FormControlLabel
            key={index}
            value={answer}
            control={<Radio />}
            label={<span dangerouslySetInnerHTML={{ __html: answer }} />}
            disabled={disabled}
          />
        ))}
      </RadioGroup>
    </div>
  );
};

export default Question;
