## Quick Start Guide

### 1. Setup Database (One-time setup)

```bash
# Connect to PostgreSQL and create database
psql postgresql://postgres@localhost:5432/postgres

# In PostgreSQL shell:
CREATE DATABASE todoapp;
CREATE USER todouser WITH ENCRYPTED PASSWORD 'todopassword';
GRANT ALL PRIVILEGES ON DATABASE todoapp TO todouser;
\q
```

### 2. Setup Project

```bash
# Clone or create project directory
mkdir fastapi-todo
cd fastapi-todo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your database credentials
echo "DATABASE_URL=postgresql://todouser:todopassword@localhost:5432/todoapp" > .env
echo "APP_NAME=My Todo App" >> .env
echo "DEBUG=True" >> .env
```

### 3. Run the Application

```bash
# Make sure PostgreSQL is running
brew services start postgresql@15  # macOS
# or
sudo systemctl start postgresql    # Linux

# Run the FastAPI app
python main.py
# or
uvicorn main:app --reload
```

### 4. Test the API

Visit: http://localhost:8000/docs

Example API calls:

```bash
# Create a todo
curl -X POST "http://localhost:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn FastAPI", "description": "Build a todo app with PostgreSQL"}'

# Get all todos
curl "http://localhost:8000/todos"

# Get statistics
curl "http://localhost:8000/todos/stats/summary"
```

---

## Troubleshooting

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL is running
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# Test connection manually
psql postgresql://todouser:todopassword@localhost:5432/todoapp
```

### Common Errors

1. **"relation does not exist"** - Tables not created. Check database connection and restart app.
2. **"password authentication failed"** - Check username/password in .env file.
3. **"could not connect to server"** - PostgreSQL service not running.
