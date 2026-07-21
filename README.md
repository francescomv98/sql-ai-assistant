# SQL AI Assistant

A Natural Language to SQL AI assistant built with LangChain, OpenAI, SQLAlchemy and SQLite.

The application allows users to ask questions about structured data using natural language. The system uses a LangChain SQL Agent to inspect the database schema, generate SQL queries, execute them against a relational database and return human-readable answers.

The goal of this project is to demonstrate the implementation of an AI agent capable of interacting with databases through tool calling, SQL generation and LLM-based reasoning.

## Features

- Natural language database querying
- LangChain SQL Agent implementation
- Automatic SQL query generation
- Database schema inspection
- SQL tool calling workflow
- SQL query execution against SQLite
- OpenAI LLM integration
- SQLAlchemy database management
- Pydantic-based configuration management
- Structured logging
- Exception handling
- Unit tests with pytest


## Architecture

The application follows a layered architecture designed to separate responsibilities between database management, AI agent logic, external services and application workflows.

```
                         User
                           |
                           v
              +---------------------------+
              | Natural Language Question |
              +---------------------------+
                           |
                           v
              +---------------------------+
              |       SQLService          |
              |---------------------------|
              | - Receive user query      |
              | - Execute agent workflow  |
              +---------------------------+
                           |
                           v
              +---------------------------+
              |     LangChain SQL Agent   |
              |---------------------------|
              | - Reasoning               |
              | - Tool calling            |
              | - SQL generation          |
              +---------------------------+
                    |              |
                    |              |
                    v              v

          +----------------+   +----------------+
          | SQL Tools      |   | OpenAI LLM     |
          |----------------|   +----------------+
          | List tables    |
          | Inspect schema |
          | Execute SQL    |
          +----------------+
                    |
                    v

              +----------------+
              | SQLite Database|
              +----------------+
                    |
                    v

              +----------------+
              | Final Answer   |
              | Explanation    |
              +----------------+
```

## How it works

The SQL AI workflow follows these steps:
1. A user asks a question using natural language.
2. The LangChain SQL Agent analyzes the available database structure.
3. The agent retrieves information about tables and schemas using SQL tools.
4. The LLM generates the required SQL query.
5. The generated SQL query is validated and executed against SQLite.
6. The query result is interpreted by the LLM.
7. A final human-readable answer is returned to the user.


## Agent Workflow

The core component of the application is the LangChain SQL Agent.
The agent is responsible for deciding which actions are required to answer a user question.
Example workflow:

```
User Question

    |
    v

"Which customers bought a Laptop?"

    |
    v

LangChain SQL Agent

    |
    +--> Inspect database tables
    |
    +--> Retrieve table schemas
    |
    +--> Generate SQL query
    |
    +--> Execute SQL query
    |
    +--> Interpret results

    |
    v

Final Answer
```

The agent uses database tools to dynamically understand the available data instead of relying on predefined SQL queries.

## Example Queries

### Question

```
How many customers are there?
```

Generated SQL:

```sql
SELECT COUNT(*) AS customer_count
FROM customers;
```

Answer:

```
There are 5 customers in the database.
```

---

### Question

```
Which customers bought a Laptop?
```

Generated SQL:

```sql
SELECT DISTINCT 
    c.id,
    c.first_name,
    c.last_name,
    c.city
FROM customers c
JOIN orders o 
    ON c.id = o.customer_id
JOIN order_items oi 
    ON o.id = oi.order_id
JOIN products p 
    ON oi.product_id = p.id
WHERE p.name = 'Laptop';
```

Answer:

```
The customers who bought a Laptop are:
- Alice Rossi from Rome
- Marco Bianchi from Milan
- Emma Brown from Paris
```

---

### Question

```
Which product generated the highest revenue?
```

Generated SQL:

```sql
SELECT 
    p.name,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN products p 
    ON oi.product_id = p.id
GROUP BY p.id
ORDER BY total_revenue DESC
LIMIT 1;
```

Answer:

```
The product that generated the highest revenue is the Laptop,
with a total revenue of 8400.0.
```

## Main Components

### SQL Agent

Responsible for the AI reasoning workflow:
- understanding user questions;
- inspecting database structure;
- generating SQL queries;
- interacting with database tools;
- producing final answers.


### SQL Service

Application service responsible for:
- receiving user requests;
- invoking the SQL Agent;
- managing the execution workflow.


### Database Layer

Handles database creation and interaction:
- SQLite initialization;
- SQLAlchemy engine management;
- LangChain SQLDatabase integration.


### OpenAI Client

Provides the LLM interface used by LangChain:
- model initialization;
- API configuration;
- communication with OpenAI.


### Configuration Management

The application uses Pydantic Settings to manage:
- environment variables;
- application configuration;
- OpenAI settings.


### Logging and Exception Handling

The project includes:
- structured application logs;
- custom exceptions;
- error handling across application layers.


## Tech Stack

### Backend

- Python
- SQLAlchemy
- SQLite

### AI / LLM

- LangChain
- LangChain SQL Agent
- OpenAI API

### Configuration

- Pydantic Settings

### Testing

- Pytest

### Development Tools

- Git
- Virtual Environment


## Project Structure

```
sql-ai-assistant/

│
├── main.py                         # Application entry point
│
├── src/
│   │
│   ├── agent/
│   │   └── sql_agent.py            # LangChain SQL Agent implementation
│   │
│   ├── config/
│   │   └── settings.py             # Application configuration
│   │
│   ├── database/
│   │   ├── db_initializer.py       # Database creation and sample data
│   │   └── database_manager.py     # Database connection management
│   │
│   ├── llm/
│   │   └── openai_client.py        # OpenAI client wrapper
│   │
│   ├── services/
│   │   └── sql_service.py          # Application service layer
│   │
│   └── utils/
│       ├── exceptions.py            # Custom exceptions
│       └── logger.py                # Logging configuration
│
├── tests/
│   ├── test_database.py             # Database tests
│   └── test_sql_service.py          # Service layer tests
│
├── database/
│   └── (generated SQLite database)
│
├── .env
├── requirements.txt
└── README.md
```


## Installation

### Requirements

- Python 3.11+
- OpenAI API key


### Clone the repository

```bash
git clone https://github.com/francescomv98/sql-ai-assistant.git

cd sql-ai-assistant
```

### Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key

CHAT_MODEL=gpt-4.1-mini
```

The application uses Pydantic Settings to load configuration values from environment variables.

## Running the Application

Start the assistant:

```bash
python main.py
```

The application will initialize the database and start an interactive session.

Example:

```
Ask a question (or type 'exit'):

How many customers are there?
```

## Testing

Run the test suite:

```bash
pytest
```

The project includes tests for:

- database initialization;
- service layer behavior;
- application components.

## Future Improvements

Possible future improvements:
- Add conversational memory
- Support multiple database engines
- Add SQL query visualization
- Store query history
- Add authentication and user management
- Add integration tests with real LLM calls
- Migrate LangChain SQL integrations to standalone packages