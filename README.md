# Algorithm-1

Algorithm 1 code repository for SENG499 Summer 2022 project.

## Contributors

- Nicole Makarowski (@nmakarowski)
- Elizabeth Vellethara (@elizabethjv)
- Tristan Slater (@trslater)
- Graham Stewart (@solidsnackdrive)
- Ty Ellison (@tyellison)
- Dana Bell (@harkken)

## Usage

To make requests to the API, you can use a 3rd-party tool (e.g., curl, Postman), or you can use the build-in API docs.

To launch interactive API documentation, navigate to `<server_address>/docs` in a browser, e.g., `http://localhost:8000/docs`.

To make a request via the interactive API docs, click on an endpoint to expand, and click "Try it out." You can now edit the provided dummy request body. Click "Execute" to send the request. Response status and data will appear below.

## Running Locally

It is recommended to run the API server via Docker:

```
docker compose up
```

If you wish to rebuild the containers, you can use:

```
docker compose up --build
```

## Heroku Deployment

Navigate to the project root.

Log into your Heroku container registry via the Heroku CLI:

```
heroku container:login
```

Create a new Heroku app:

```
heroku create
```

Then deploy and release the app:

```
heroku container:push web
heroku container:release web
```

You can then easily open the deployed app:

```
heroku open
```

## API Generation Tool

> :warning: This tool is meant only to assist in generating function definitions and Pydantic models. Do not directly overwrite the actual codebase's `main.py` or `models.py`. These contain additional logic that would be erased.

There is FastAPI code generator tool (added to `requirements.txt`) that generates FastAPI endpoint definitions and Pydantic models for FastAPI from an OpenAPI spec:

```
fastapi-codegen -i openapi.json -o temp/
```

`main.py` and `models.py` should appear in your `temp/` directory. You can use these as a guide to make sure the API code is adhering to the OpenAPI spec.

## Logging

The loggers are set up to be children of the main application logger: `algo1`. To create a logger for a module:

```
import logging

logger = logging.getLogger(__name__)
```

Because everything is a child module of `algo1`, the loggers will all be child loggers of the main `algo1` logger. For example, if you call `logging.getLogger(__name__)` in the `algo1/api/main.py` file, the logger will be named `algo1.api.main` (the same as `__name__`). If `algo.api` logger exists, it will become the parent of `algo.api.main`, and `algo1` will be the parent of `algo1.api`. Otherwise, `algo1` will be the parent of `algo.api.main`. This happens automatically and greatly simplifies logging config and usage.

Now, anywhere you would use a `print` statement, use `logger.critical`, `logger.error`, `logger.warning`, `logger.info`, or `logger.debug` in its place.

The default log level is `DEBUG`. This gives lots of info to work with in these early development stages. If you'd like to lower the log level during development to calm down the terminal, you can override the environment variable when running the API:

```
LOG_LEVEL=WARNING python -m algo1.api.run
```

Change `WARNING` to the desired log level.
