# SW3-GRP5-PROJECT

Final Group Project for Software-3-Group-5

Welcome to our repository. We have created a Trivia Quiz game!

Instructions on how to run our trivia game programme:

1. In your terminal, navigate to a directory/folder on your machine where you would like to clone this repo to. Execute the command: `git clone git@github.com:hvuvuzella/SW3-GRP5-PROJECT.git`

2. Then navigate to the project by executing `cd SW3-GRP5-PROJECT`

3. Open the project in PyCharm CE(`open -a "PyCharm CE" .`), as well as VSCode(`code .`). You may need to change the terminal commands depending on the operating system you use.

In the project directory, you will see all of our folders and files. All of the Frontend files are in the front-end folder, and all of the unit test files are in the unit_tests folder. For the Backend files, we have kept them all in the project's main directory for ease of use and visibility when running the files.

TO RUN THE BACKEND OF THE PROGRAMME:

4. You will see the trivia_game.sql file in the main directory. Initialise the database (DB) by running this script in MySQL Workbench.

5. In PyCharm CE, go to the config.py file, and edit it by replacing the USER and PASSWORD values with your personal MySQL login user and password. This will open the connection between the BE and the DB.

6. Then, run the DB_utils.py file to establish the BE connection to the DB. There are some quick example test runs of the DB functions within this file which prints outcomes in the console for you to see what to expect in terms of return values. After running this file, you can go back to the trivia_game.sql file in MySQL Workbench and run the SELECT \* queries at the bottom of the file to see changes to the DB to help you understand how the DB functions work.

7. Then, to establish the BE Flask app endpoints, go ahead and run app.py file in Pycharm CE.

8. TO RUN FE SIMULATION IN PYTHON:
- run main.py and play the quiz game from within in the python console. We also have created a FE for the game to played on the web browser. To play the game in the browser, go to step 9:

9. TO RUN THE FRONTEND OF OUR PROGRAMME ON A WEBPAGE:

- Ensure you have Node.js installed on your machine. You can download it from https://nodejs.org/.
- Open a new terminal window and navigate to the project's directory. Navigate to the project's directory on your local machine again, and then to the front-end folder, using the following command:
  `cd front-end`
- Install Node Package Manager (NPM) dependencies using the following command:
  `npm install`
  This will download and install the necessary packages required for the project.
- Start the frontend application using the following command:
  `npm start`
  This command initiates the development server, compiles the React application, and opens it in your default web browser. The application will automatically reload if you make changes to the source code. You may also see any lint errors in the console. This runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

- Running `npm test` launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.
 
