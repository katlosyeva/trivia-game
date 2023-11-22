import { FormControlLabel, Radio, RadioGroup, Typography } from "@mui/material";

const Question = ({
  question,
  answers,
  selectedAnswer,
  onChange,
  disabled,
}) => (
  <div>
    <Typography variant="h5">{question}</Typography>
    <RadioGroup
      aria-label="answers"
      name="answers"
      value={selectedAnswer}
      onChange={onChange}
      disabled={disabled}
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
  </div>
);

export default Question;
