# Install and run the server locally

1. Have a PostgreSQL database running locally, with the following environment variables set:

```bash
POSTGRES_USER=demo
POSTGRES_PASSWORD=demo
POSTGRES_DB=demo
```

Or you can use the service in `docker-compose` file in root folder by running

``` bash
cd ..
docker-compose up -d db
```

2.Have poetry installed, then run the following commands to install the dependencies and run the migrations:

```bash
poetry install
poetry run alembic upgrade head
```

Then, run the following commands:

```bash
poetry run uvicorn server.web.application:get_app
```

## View the API documentation

Launch the server, then go to [http://localhost:8000/docs](http://localhost:8000/docs)

Key endpoints:

- `POST /contacts` — create a contact (requires name and email)
- `GET /contacts` — list contacts
- `GET /contacts/by-email?email=you@example.com` — find contact by email
- `GET /contacts/{name}` — get a contact by name

## Run the unit tests

```bash
poetry run python -m unittest discover
```
