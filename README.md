# Descartes Underwriting - Technical test

This project template using ReactJS & Python that can be used for Descartes Underwriting technical test.

To install and run this project:

```
docker-compose up --build
```

The first install and run will take a while, because it will install all the dependencies and build the images.
Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

To run separately the server or client, please see the README.md in the server and client folders.

# Demo

https://github.com/valeeraZ/descartes-app/assets/39196828/ec9373bd-5797-46e6-94e8-e57cddd863ba


# Architecture
![archi-descartes](https://github.com/valeeraZ/descartes-app/assets/39196828/c953f735-4668-4f02-87c0-b5f282a30839)


The server is a FastAPI application that uses a PostgreSQL database. The client is a React application with Next.js that uses the server API.

For the server, the FastAPI uses a router to handle the requests. The router uses a query service and a command service to handle the business logic with the contact read model and write model. The service uses a repository to access a PostgreSQL database by CRUD actions with SQLAlchemy models.

# CI/CD


The CI/CD is done with Github Actions. The workflow is triggered on push and pull request on the main branch. The workflow will run the unit tests and the linter of the code in server.

# Instructions

## Submission

The solution to this test (source and test codes) should be saved on a private `descartes-app` repository on your github account.

Access should be granted to:

- [https://github.com/alexandreCameron](https://github.com/alexandreCameron)
- [https://github.com/f-combes](https://github.com/f-combes)
- [https://github.com/achilleas-michos](https://github.com/achilleas-michos)
- [https://github.com/michelclet](https://github.com/michelclet)

## Duration

Preparing the test should take 3 to 5 hours.

## Task

Create a simple 3-tier application to manage contacts.

The application should allow the user to:

1. List the existing contacts
2. View the details of a contact
3. Create a new contact (fields: first name, last name, job, address, question)

Technology stack recommended:

1. React for the frontend
2. Python for the backend (e.g. fastapi, flask)
3. Database (any type that can store this type of data)
4. Docker files and docker compose

The project should contain:

1. `README.md` with the commands to install and run the app locally
2. A diagram of the architecture (component and interaction)
3. A minimal CI/CD to check the code quality before integration on main branch

## Comment

Anything that is not listed in the task section does not have to be developed.
No need to bother with access management, signing etc.

Testing should exist but remain minimal, just for demonstration purposes.
