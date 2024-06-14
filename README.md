# Strategy App

## Running locally with docker compose

Prerequisites:
- WSL2 installed if on Windows
- Docker Desktop installed

From the root of the repository, run `docker-compose up --build -d` to start the application. This will build the image (`--build`), start the containers (`up`), and run in detached mode (`-d`) so that you get your command line back.

Once the application is up and running, you can view it at `localhost:8000`.

If you need to run database migrations, run `docker-compose exec web python manage.py migrate` to execute all of the migrations available.