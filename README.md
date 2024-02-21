# Trivia-game

## Overview

This project is a full-stack application built with React for the front end, Flask for the back end, and a SQL database. It's designed to run both as standalone services and as a unified application using Docker. Additionally, Kubernetes configurations are provided for deploying the project in a Kubernetes cluster.

## Running Standalone Services

### Frontend:

- Navigate to the frontend directory.
- Install dependencies: `npm install`.
- Start the frontend: `npm start`.

### Backend:

- Navigate to the backend directory.
- Install dependencies: `pip install -r requirements.txt`.
- Run the Flask app: `python app.py`.
- In the backend folder, change your SQL credentials in the `config.py` file.

### Database:

- Set up a SQL database server and execute SQL scripts to create the necessary tables and schema.

## Running with Docker

- Ensure Docker is installed on your machine.
- In the backend folder, change `HOST` to "mysql".
- Run the following command in the root directory. This will build and start Docker containers for the frontend, backend, and database:

  ```bash
  docker-compose up

## Running with Kubernetes

Kubernetes configurations are provided in the kubernetes directory.

- Apply the configurations to your Kubernetes cluster:

  ```bash
  kubectl apply -f kubernetes/

## Once the services are running, access the application in your web browser:

Frontend: http://localhost:3000 (For k8s - http://localhost:31515)
Backend: http://localhost:5000

## Swagger Documentation

- Swagger documentation for the API can be accessed at: http://localhost:5000/api/docs/
- Developers can use this Swagger documentation to understand and interact with the backend API independently and create their own custom frontend.

## Cleanup

- Stop and remove Docker containers:

  ```bash
  docker-compose down

- Delete Kubernetes resources:

  ```bash
  kubectl delete -f kubernetes/

## VIDEO DEMO OF THE GAME:
- A shortened version of the game (5 questions instead of 15), for you to see:

https://drive.google.com/file/d/1DKkOSjQcEPIKJ_nX3z8JYdGel0AMTfZO/view?usp=sharing







Overview

This project is a full-stack application built with React for the front end, Flask for the back end, and a SQL database. It's designed to run both as standalone services and as a unified application using Docker. Additionally, Kubernetes configurations are provided for deploying the project in a Kubernetes cluster.

Running Standalone Services

Frontend:
- Navigate to the frontend directory.
- Install dependencies: npm install.
- Start the frontend: npm start.

Backend:
- Navigate to the backend directory.
- Install dependencies: pip install -r requirements.txt.
- Run the Flask app: python app.py.

Database:
- In the backend folder change you SQL credentials in config.py file 
- Set up a SQL database server and execute SQL scripts to create the necessary tables and schema.

Running with Docker
- Ensure Docker is installed on your machine.
- In the backend folder change HOST to "mysql"
- Run the following command in the root directory:

docker compose-up

This will build and start Docker containers for the frontend, backend, and database.

Running with Kubernetes

Kubernetes configurations are provided in the kubernetes directory.
Apply the configurations to your Kubernetes cluster:

kubectl apply -f kubernetes/
Accessing the Application
Once the services are running, access the application in your web browser:

Frontend: http://localhost:3000 (For k8s - http://localhost:31515)
Backend: http://localhost:5000

Swagger Documentation

- Swagger documentation for the API can be accessed at: http://localhost:5000/api/docs/
- Developers can use this Swagger documentation to understand and interact with the backend API independently and create their own custom frontend.

Cleanup

Stop and remove Docker containers:
docker-compose down

Delete Kubernetes resources:
kubectl delete -f kubernetes/

VIDEO DEMO OF THE GAME:
- A shortened version of the game (5 questions instead of 15), for you to see:

https://drive.google.com/file/d/1DKkOSjQcEPIKJ_nX3z8JYdGel0AMTfZO/view?usp=sharing
