# Install and run the server locally

1. Have a PostgreSQL database running locally, with the following environment variables set:

```bash
POSTGRES_USER=descartes
POSTGRES_PASSWORD=descartes
POSTGRES_DB=descartes
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

# View the API documentation

Launch the server, then go to [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

# Run the unit tests


```bash
poetry run python -m unittest discover
```
