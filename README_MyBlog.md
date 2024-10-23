
# MyBlog - Blog Application

Created a blog application where administrator can post articles, pages, and interact with content. The project is deployed using Docker containers on Google Cloud Platform.

## Table of Contents
1. [Project Description](#project-description)
2. [Technologies](#technologies)
3. [Project Highlights](#project-highlights)
4. [Deployment](#deployment)
5. [How to Run Locally](#how-to-run-locally)
6. [Repository](#repository)

## Project Description
MyBlog is a full-featured blog application developed with Django, allowing users to create, publish, and comment on articles. The project is containerized with Docker and deployed on Google Cloud Platform, ensuring scalability and ease of deployment.

## Technologies
- **Python**
- **Django**
- **PostgreSQL**
- **HTML**
- **Bootstrap**
- **Docker**
- **Google Cloud Platform (GCP)**

## Project Highlights
- **User-Friendly Blog**: Administrator can create accounts, post articles, pages, and interact with the content.
- **PostgreSQL Database**: The blog uses PostgreSQL as the database, ensuring robust and scalable data storage.
- **Containerized Deployment**: Docker is used to containerize the application, simplifying the deployment process.
- **Deployed on GCP**: The application is hosted on Google Cloud Platform, leveraging cloud services for high availability and performance.

## Deployment
The project is deployed on Google Cloud Platform using Docker containers. The application is set up with PostgreSQL for data storage and runs inside Docker containers for easy scalability and maintenance.

## How to Run Locally
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Jaycmarques/MyBlog.git
   cd MyBlog
   ```

2. Build the Docker containers:
   ```bash
   docker-compose build
   ```

3. Start the Docker containers:
   ```bash
   docker-compose up
   ```

4. Run migrations: Open a new terminal window (keeping the previous one running) and execute:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. Open your browser and go to `http://localhost:8000` to view the site locally.

