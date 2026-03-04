# Project Overview

This is a Python Flask web application designed to manage "coffee requests" and user balances. It uses a MySQL database for data persistence and is containerized with Docker and Docker Compose for easy setup and deployment. The application allows users to check their coffee balance and submit requests, which are then processed and trigger email notifications.

## Technologies Used

*   **Backend:** Python 3.11, Flask
*   **Database:** MySQL
*   **Dependency Management:** `uv`
*   **Containerization:** Docker, Docker Compose
*   **Email Notifications:** `smtplib`

## Building and Running

### Local Development

To set up and run the application locally using Docker Compose for development:

1.  **Environment Variables:** Create a `.env` file in the project root directory, similar to `deploy/.env.example`, and fill in the necessary database credentials and `APP_PASSWORD` for email notifications.
    ```
    DB_HOST="db"
    MYSQL_DATABASE="app-db"
    MYSQL_USER="arabica"
    MYSQL_PASSWORD="your_mysql_user_password"
    MYSQL_ROOT_PASSWORD="your_mysql_root_password"
    APP_PASSWORD="your_email_app_password"
    ```
    *   `APP_PASSWORD` is an application-specific password for your email account, required for `sender_email` to send notifications.
    *   `DB_HOST` should be `db` when running with Docker Compose.
2.  **Initialize Database:** The `init_db/full_backup.sql` script will be automatically executed when the `db` service starts for the first time.
3.  **Run with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    This will build the `app` image, start the MySQL database, and run the Flask application. The application will be accessible at `http://localhost:5000`.

### Deployment

For deployment, an alternative `docker-compose.yml` is provided in the `deploy/` directory, which uses a pre-built Docker image for the application.

1.  **Environment Variables:** Create a `.env` file in the `deploy/` directory based on `deploy/.env.example` with your production environment variables.
2.  **Run Deployment Docker Compose:**
    ```bash
    docker-compose -f deploy/docker-compose.yml up -d
    ```
    This will pull the pre-built `skynet214/remote-coffee-app:latest` image and run the application in detached mode.

## Configuration

The application relies on environment variables for configuration, particularly for database connection details and email credentials. These are loaded from `.env` files.

## Application Structure

*   `app/`: Contains the main Flask application code, templates, and static assets.
    *   `app.py`: The main Flask application file, defining routes, database interactions, and email sending logic.
    *   `templates/`: HTML templates (e.g., `index.html`).
    *   `static/`: Static files like CSS, JavaScript, and images.
*   `deploy/`: Contains deployment-specific configurations.
    *   `docker-compose.yml`: Docker Compose file for deployment, using a pre-built image.
    *   `.env.example`: Example environment variables for deployment.
*   `init_db/`: Contains SQL scripts for initializing the database.
    *   `full_backup.sql`: Database schema and initial data.
*   `pyproject.toml`: Project metadata and Python dependencies managed by `uv`.
*   `Dockerfile`: Defines the Docker image for the Flask application.
*   `docker-compose.yml`: Docker Compose file for local development.
*   `.env`: (Ignored by Git) Environment variables for local development.
*   `.gitignore`: Specifies intentionally untracked files to ignore.
*   `.dockerignore`: Specifies files and directories to exclude when building Docker images.
