DROP DATABASE IF EXISTS trivia_game;
-- create database:
CREATE DATABASE trivia_game;

USE trivia_game;

-- create normalised tables:
CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(40) NOT NULL
);

CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
	score INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
	game_id INT,
	question_text VARCHAR(300) NOT NULL,
	FOREIGN KEY (game_id) REFERENCES games(id)
);

CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
	question_id INT,
	answer_text VARCHAR(150) NOT NULL,
	FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE correct_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
	question_id INT,
	correct_answer_id INT,
	FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (correct_answer_id) REFERENCES answers(id)
);

