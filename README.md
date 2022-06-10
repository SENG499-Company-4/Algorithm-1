# Algorithm-1
Algorithm 1 code repository for SENG499 Summer 2022 project.

## Contributors
- Nicole Makarowski (@nmakarowski)
- Elizabeth Vellethara (@elizabethjv)
- Tristan Slater (@trslater)
- Graham Stewart (@solidsnackdrive)
- Ty Ricard (@tyricard)

## Server Usage

```
uvicorn main:app --reload
```

To launch API documentation, navigate to `<server_address>/docs` in a browser, e.g., `http://localhost:8000/docs`.

To use: 

1. Run the server: `uvicorn main:app --reload`
2. Use some sort of rest client such as Postman, curl, or Thunder Clint and make a POST request to http://localhost:8000/generate
3. Output will be preference data in JSON format!
