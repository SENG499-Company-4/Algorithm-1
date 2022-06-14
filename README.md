# Algorithm-1
Algorithm 1 code repository for SENG499 Summer 2022 project.

## Contributors
- Nicole Makarowski (@nmakarowski)
- Elizabeth Vellethara (@elizabethjv)
- Tristan Slater (@trslater)
- Graham Stewart (@solidsnackdrive)
- Ty Ellison (@tyellison)
- Dana Bell (@harkken)

## Server Usage

```
uvicorn main:app --reload
```

To make requests to the API, you can use a 3rd-party tool (e.g., curl, Postman), or you can use the build-in API docs.

To launch interactive API documentation, navigate to `<server_address>/docs` in a browser, e.g., `http://localhost:8000/docs`.

To make a request via the interactive API docs, click on an endpoint to expand, and click "Try it out." You can now edit the provided dummy request body. Click "Execute" to send the request. Response status and data will appear below.
