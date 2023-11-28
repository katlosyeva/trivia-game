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

6. Then, run the DB_utils.py file to establish the BE connection to the DB. There are some quick example test runs of the DB functions within this file which prints outcomes in the console for you to see what to expect in terms of return values. After running this file, you can go back to the trivia_game.sql file in MySQL Workbench and run the SELECT * queries at the bottom of the file to see changes to the DB to help you understand how the DB functions work.

7. Then, to establish the BE Flask app endpoints, go ahead and run app.py file in Pycharm CE.

8. TO RUN THE FRONTEND OF OUR PROGRAMME:

   - Please ensure you have node.js installed first
   - Open a new terminal window and navigate to the project's directory again, and run the following commands:
   - `cd front-end` (to navigate to the front-end folder)
   - `npm i` (to install Node Package Manager library)
   - `npm start` (Erika please add what this means)
