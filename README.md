# Google Keep Clone

FastAPI-based backend for a Google Keep Clone, leveraging MongoDB and Pydantic for efficient data management. Easily
deployable with Docker, and ready for integration with your preferred frontend framework.

> **This is developed with beta version of FastAPI and Pydantic, and is subject to change. Modify and make the necessary
changes to the code to make it work with the latest versions.**

## Installation

1. Clone the repository
2. Install Docker and Docker Compose
3. Run `docker-compose up --build`
4. Go to `http://localhost:8000/docs` to see the API documentation

## Features and TODOs

- [x] Create, read, update, and delete notes
- [x] Create, read, update, and delete labels
- [x] Add and remove labels from notes
- [x] Search notes by title, content, or label
- [x] Filter notes by label
- [x] Filter notes by pinned status
- [x] Upload image for notes
