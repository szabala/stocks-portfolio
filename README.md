# stocks-portfolio

## Introduction
This project consists of a FastAPI application that serves as a backend for a stock portfolio. It allows users to create, read and rebalance their stock portfolios.

## Application Architecture
This application follows a layered architecture. It's divided into 4 main layers:
- **Entry Layer**: FastAPI application, routers, and API schemas.
- **Application Layer**: Application services that interact with the domain and infrastructure.
- **Domain Layer**: Domain models and aggregates that represent the core business entities.
- **Infrastructure Layer**: Infrastructure implementations such as repositories and external APIs.

Here is a brief rundown of the project structure:

- `main.py`: Application entry point.
- `routers/`: FastAPI routers and API schemas.
- `application/`: Application services.
- `domains/`: Domain models and aggregates.
- `ports/`: Abstract interfaces mainly for infrastructure.
- `infrastructure/`: Infrastructure implementations such as repositories and external APIs.
- `exceptions/`: Custom exception classes.

## How to Run
### Application
To run the application, you can use Docker. Make sure you have Docker and Docker Compose installed on your machine.

```sh
docker-compose up --build
```

This will start the FastAPI application on `http://localhost:8000`.

### Tests
This project uses `pytest` for unit testing. You can run the tests with:

```sh
pytest
```

## Docs
The application automatically generates OpenAPI documentation. You can access it at:

- [http://localhost:8000/docs](http://localhost:8000/docs)

If you don't want to run the application, you can view the API documentation in [Swagger Editor](https://editor.swagger.io/?url=https://raw.githubusercontent.com/szabala/stocks-portfolio/refs/heads/main/docs/openapi.json).
