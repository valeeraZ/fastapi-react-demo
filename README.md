# FastAPI Demo App

This is a simple 3-tier application to manage contacts. The application allows the user to:

1. List the existing contacts
2. View the details of a contact
3. Create a new contact (fields: first name, last name, job, address)

It is built with:

- FastAPI for the backend with async SQLAlchemy and Alembic for migrations
- PostgreSQL for the database

To install and run this project:

```
docker-compose up --build
```
