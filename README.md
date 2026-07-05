# solution-Kristian_Schnapp

# Ticket API

FastAPI application for managing tickets and users.

The application fetches users and todos from DummyJSON, stores them in a local SQLite database, and exposes REST API endpoints for listing, searching, filtering, creating, and updating tickets.

## Technologies

- Python
- FastAPI
- SQLAlchemy async
- SQLite
- Pydantic
- HTTPX

## Project structure

```text
solution-Kristian_Schnapp/
├── src/
│   ├── main.py
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   ├── helpers.py
│   └── schemas.py
├── requirements.txt
├── Makefile
├── README.md
└── .gitignore
```

## project setup 

- create a python virtual environment using python -m venv (path to the virtual environment or just . to create it in your current directory)
- Activate the virtual environment by going to the Scripts folder and running the activate script for your operating system
- Use command cd .. to get out of Scripts directory
- run command pip install -r requirements.txt to install the required packages
- run python src/main.py to run the application


## Endpoints

### GET
- /tickets (get all tickets)
- /tickets/{id} (get a ticket by id)
- /tickets/?priority=&status= (filter tickets by priority and status)
- /tickets/search?search_query= (filter tickets by todo content)


### POST
- /tickets (create a new ticket)

```
Request body example

{
  "todo": "string",
  "completed": true,
  "userId": 9
}

```

### PATCH
- /tickets/{id} (update a ticket)

```
Request body example
{
  "todo": "string",
  "completed": true,
  "userId": 9
}

```