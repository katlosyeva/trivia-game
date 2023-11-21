/*  
NOTES FOR GROUP 5 team members:

FLOW OF GAME: 

1. ASKED IF NEW PLAYER OR EXISITNG:
	- IF NEW: ask player to create a username and ADD TO Players table, and player id = id WHERE username = "new username"
    - IF EXISITNG: player id = id WHERE username = "given username'
2. ASKED TO START GAME? 
    - IF NO: exit
    - IF YES: START GAME: INSERT player_id to games table

3. RUN GAME():
   - AT BEGINNING OF GAME: CALL API and get JSON response:
        - populate questions into questions table (game_id, player_id, difficulty_level, question_text, correct_answer, incorrect_answer_1,
          incorrect_answer_2, incorrect_answer_3)
        - AT SAME TIME: populate game_questions table (game_id, player_id, question_id, player_answer(NULL), correct_answer, is_correct(NULL)
        - ALSO AT SAME TIME: populate scoreboard table (game_id, player_id, total_score(0))

   - AFTER EACH QUESTION ITERATION IN GAME where player_answer is retrieved:
       - update exisitng game_question row to SET player_answer from NULL to answer, and calculate if correct or not for is_correct column
        - AT SAME TIME: update existing SCOREBOARD row of data to SET TOTAL_SCORE from current accumulated total_score to value of SUM of TRUE = 1's and False = 0's (see UPDATE query below),
          e.g. 0 + 0 + 1 + 1 + 1 by the time player answers 5th question
*/


DROP DATABASE IF EXISTS trivia_game;
-- create database:
CREATE DATABASE trivia_game;

USE trivia_game;

-- create normalized tables:
CREATE TABLE players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(40) NOT NULL
);

CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    difficulty_level VARCHAR(10) NOT NULL,
    question_text VARCHAR(300) NOT NULL,
    correct_answer VARCHAR(100) NOT NULL,
    incorrect_answer_1 VARCHAR(100) NOT NULL,
    incorrect_answer_2 VARCHAR(100) NOT NULL,
    incorrect_answer_3 VARCHAR(100) NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

CREATE TABLE game_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    player_id INT,
    question_id INT,
    player_answer VARCHAR(100), -- store the user's answer
    correct_answer VARCHAR(100), -- store the correct answer for reference - as Iryna originally included. This helps to not need to join two tables to evaluate is_correct as we have included it in this table too from the start.
    is_correct BOOLEAN, -- check if answer is correct
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE scoreboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    player_id INT,
    total_score INT,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- AT START OF GAME(1):
-- example of inserting new questions data to questions table when APU is called, and also inserting game_id and player_id as 
-- we will know game_id and player_id from already registering player and starting game:
INSERT INTO questions (game_id, player_id, difficulty_level, question_text, correct_answer, incorrect_answer_1, incorrect_answer_2, incorrect_answer_3)
VALUES 
    (1, 1, 'medium', 'Who won the 2011 Stanley Cup?', 'Boston Bruins', 'Montreal Canadiens', 'New York Rangers', 'Toronto Maple Leafs'),
    (1, 1, 'easy', 'What is the maximum level you can have in a single class in Dungeons and Dragons (5e)?', '20', '30', '15', '25'),
    (1, 1, 'easy', 'What company developed the vocaloid Hatsune Miku?', 'Crypton Future Media', 'Sega', 'Sony', 'Yamaha Corporation');
    

-- AT START OF GAME(2):
-- Assuming you have the necessary game and player information (created one player registers, and game starts)
INSERT INTO game_questions (game_id, player_id, question_id, correct_answer, player_answer, is_correct)
SELECT 
    1 AS game_id,  -- Replace with the actual game ID. use {} as placeholders in Python code instead of the 1 shown here for game_id
    1 AS player_id,  -- Replace with the actual player ID. use {} as placeholders in Python code instead of the 1 shown here from player_id
    id AS question_id,
    correct_answer,
    NULL AS player_answer,
    NULL AS is_correct
FROM questions;

-- AT START OF GAME(3):
-- Populate Scoreboard table at the start of every game (i.e. when API is called, with intial total_score is set to zero, and then updates
-- after every time player answers each question)
INSERT INTO scoreboard (game_id, player_id, total_score)
VALUES (1, 1, 0); -- Replace with actual game_id and player_id, then:



/*-- AFTER EACH QUESTION(1):
-- UPDATE game_questions row for that question
-- We already have the necessary game_id and player_id
-- The question_id is the ID of the question being answered
-- WE HAVE JUST retrieved player_answer which is the answer given by the player
-- AND is_correct is a boolean indicating whether the answer is correct or not: */
UPDATE game_questions
SET 
    player_answer = 'Boston Bruins',  -- Replace with the actual player's answer
    is_correct = TRUE  -- Replace with the actual boolean indicating correctness (need to write a python function to evaulate player_answer against correct_answer in game_questions table)
WHERE
    game_id = 1  -- Replace with the actual game_id - THIS STAYS THE SAME IN THE WHOLE GAME
    AND player_id = 1  -- Replace with the actual player_id - THIS STAYS THE SAME IN THE WHOLE GAME
    AND question_id = 1;  -- Replace with the actual question_id - THIS CHANGES AFTER EACH QUESTION IN THE GAME
    
/*
-- AFTER EACH QUESTION(2):
-- THEN, UPDATE scoreboard row for that game:
-- (after EACH QUESTION is answered by the player through their game, update total_score): 
-- (to adapt in Python BE later): */
UPDATE scoreboard sb
-- Set(i.e.change) total_score to the accumulated sum of correct answers in the game_questions table up to the current question.
SET total_score = (
    -- Calculate the sum of correct answers (1 for TRUE, 0 for FALSE). CAST converts boolean TRUE to 1, FALSE to 0.
    SELECT SUM(CAST(is_correct AS SIGNED))
    -- Select rows from the game_questions table for the specific game_id
    FROM game_questions
    WHERE game_id = sb.game_id AND player_id = sb.player_id -- MAKE SURE game_id and player_id is correct for the current game being played.
);


-- LEADERBOARD TO DISPLAY: (we don't need to create a new table for leaderboard - just select top 10 scores):
-- example of using SELECT query to get top 10 scores to display on the Leaderboard
SELECT *
FROM scoreboard
ORDER BY total_score DESC
LIMIT 10;