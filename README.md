# Sport League 

This guide explains how to run the Sport League project using Docker . By following these steps, you'll be able to set up the project environment and access it through your browser.

## Prerequisites

Before you begin, ensure that you have the following software installed on your machine:

- Docker
- Docker Compose

## Steps

1. **Clone the Project**

   Clone the Sport League project repository from the desired source, such as GitHub.

   ```shell
   git clone https://github.com/ahmadcasper2018/sports-league.git

2. **Navigate to the Project Directory**

   Open your terminal and navigate to the directory where you cloned the Sport League project.

3. Build the Docker Image

   Build the Docker image by running the following command:

   ```shell
   docker-compose build
   


   
4. Setup API environment variable 
   create .env file in frontend directory and add you Endpoint

   ```shell
   REACT_APP_API_BASE_URL=http://127.0.0.1:8000
   
5. Start the Container

   Start the container by running the following command:

   ```shell
   docker-compose up

6. Access the Project
   After successfully starting the container, you can access the Sport League project in your browser by visiting http://localhost:3000
.

**note**: there is 41 tests in the project sometimes they are not all tracked with docker backend container, in this case you need to run:
* python manage.py test accounts
* python manage.py test games/tests/