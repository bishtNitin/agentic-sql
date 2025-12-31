# API Documentation

Complete reference for Agentic SQL REST API endpoints.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Currently, no authentication is required. For production deployment, consider adding:
- API keys
- JWT tokens
- OAuth 2.0

## Endpoints

### Root Endpoint

#### GET /

Root endpoint with API information.

**Response**:
```json
{
  "message": "Agentic SQL API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/health"
}
```

---

### Health Check

#### GET /api/health

Check API health and status.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "database_connected": true,
  "llm_provider": "huggingface"
}
```

**Response Fields**:
- `status`: Overall system status ("healthy", "degraded", "unhealthy")
- `timestamp`: Current server time
- `database_connected`: Database connection status
- `llm_provider`: Active LLM provider

**Example**:
```bash
curl http://localhost:8000/api/health
```

---

### Execute Query

#### POST /api/query

Execute a natural language query.

**Request Body**:
```json
{
  "query": "Show all employees with salary greater than 50000"
}
```

**Request Fields**:
- `query` (required): Natural language question

**Response** (200 OK):
```json
{
  "success": true,
  "sql_query": "SELECT * FROM employees WHERE salary > 50000",
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "department": "Engineering",
      "salary": 75000,
      "hire_date": "2020-01-15"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "department": "Sales",
      "salary": 65000,
      "hire_date": "2019-03-20"
    }
  ],
  "columns": ["id", "name", "department", "salary", "hire_date"],
  "row_count": 2,
  "execution_time": 0.145,
  "error": null
}
```

**Response Fields**:
- `success`: Whether the query was successful
- `sql_query`: Generated SQL query
- `results`: Array of result rows (as objects)
- `columns`: Array of column names
- `row_count`: Number of rows returned
- `execution_time`: Execution time in seconds
- `error`: Error message if failed (null if successful)

**Error Response** (200 OK with success: false):
```json
{
  "success": false,
  "sql_query": "SELECT * FROM nonexistent_table",
  "results": null,
  "columns": null,
  "row_count": 0,
  "execution_time": 0.023,
  "error": "no such table: nonexistent_table"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show all employees"}'
```

**Example (Python)**:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/query",
    json={"query": "Count employees by department"}
)
data = response.json()
print(data['sql_query'])
print(data['results'])
```

**Example (JavaScript)**:
```javascript
fetch('http://localhost:8000/api/query', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    query: 'Show top 5 products by price'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

### Get Database Schema

#### GET /api/schema

Retrieve database schema information.

**Response** (200 OK):
```json
{
  "tables": [
    {
      "table_name": "employees",
      "columns": [
        {"name": "id", "type": "INTEGER"},
        {"name": "name", "type": "VARCHAR(100)"},
        {"name": "department", "type": "VARCHAR(50)"},
        {"name": "salary", "type": "INTEGER"},
        {"name": "hire_date", "type": "DATE"}
      ]
    },
    {
      "table_name": "departments",
      "columns": [
        {"name": "id", "type": "INTEGER"},
        {"name": "name", "type": "VARCHAR(50)"},
        {"name": "budget", "type": "INTEGER"},
        {"name": "manager_id", "type": "INTEGER"}
      ]
    }
  ]
}
```

**Response Fields**:
- `tables`: Array of table schema objects
  - `table_name`: Name of the table
  - `columns`: Array of column objects
    - `name`: Column name
    - `type`: Column data type

**Example**:
```bash
curl http://localhost:8000/api/schema
```

---

### List Tables

#### GET /api/tables

Get a list of all database tables.

**Response** (200 OK):
```json
{
  "tables": [
    "employees",
    "departments",
    "products",
    "customers",
    "orders"
  ]
}
```

**Response Fields**:
- `tables`: Array of table names

**Example**:
```bash
curl http://localhost:8000/api/tables
```

---

### Get Query History

#### GET /api/history

Retrieve recent query history.

**Query Parameters**:
- `limit` (optional): Maximum number of history items (default: 50)

**Response** (200 OK):
```json
{
  "history": [
    {
      "id": 1,
      "natural_query": "Show all employees",
      "sql_query": "SELECT * FROM employees",
      "success": true,
      "timestamp": "2024-01-01T10:30:00.000Z"
    },
    {
      "id": 2,
      "natural_query": "Count employees by department",
      "sql_query": "SELECT department, COUNT(*) FROM employees GROUP BY department",
      "success": true,
      "timestamp": "2024-01-01T10:32:15.000Z"
    }
  ],
  "total": 2
}
```

**Response Fields**:
- `history`: Array of history items
  - `id`: History item ID
  - `natural_query`: Original natural language query
  - `sql_query`: Generated SQL
  - `success`: Whether query succeeded
  - `timestamp`: Query execution time
- `total`: Total number of history items

**Example**:
```bash
# Get last 20 queries
curl http://localhost:8000/api/history?limit=20
```

---

## Error Responses

### 500 Internal Server Error

```json
{
  "detail": "Internal server error message"
}
```

### 422 Unprocessable Entity

Returned when request validation fails.

```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production:

**Recommended Limits**:
- 100 requests per minute per IP
- 1000 requests per hour per IP

**Implementation** (using slowapi):
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/query")
@limiter.limit("10/minute")
async def execute_query(...):
    ...
```

---

## CORS

CORS is configured to allow requests from specified origins.

**Configuration** (.env):
```bash
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
**Allowed Headers**: All
**Credentials**: Enabled

---

## Webhook Support

*Not currently implemented*

For production, consider adding webhooks for:
- Long-running queries
- Query completion notifications
- Error alerts

---

## Example Use Cases

### Use Case 1: Simple Query

```bash
# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How many employees do we have?"}'

# Response
{
  "success": true,
  "sql_query": "SELECT COUNT(*) as count FROM employees",
  "results": [{"count": 50}],
  "columns": ["count"],
  "row_count": 1,
  "execution_time": 0.082
}
```

### Use Case 2: Join Query

```bash
# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show employees and their departments"}'

# Response
{
  "success": true,
  "sql_query": "SELECT e.name, d.name as department FROM employees e JOIN departments d ON e.department = d.name",
  "results": [
    {"name": "John Doe", "department": "Engineering"},
    {"name": "Jane Smith", "department": "Sales"}
  ],
  "row_count": 50,
  "execution_time": 0.234
}
```

### Use Case 3: Aggregation

```bash
# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the average salary by department?"}'

# Response
{
  "success": true,
  "sql_query": "SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department",
  "results": [
    {"department": "Engineering", "avg_salary": 85000},
    {"department": "Sales", "avg_salary": 65000},
    {"department": "Marketing", "avg_salary": 62000}
  ],
  "row_count": 5,
  "execution_time": 0.156
}
```

### Use Case 4: Complex Filter

```bash
# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show engineers hired after 2020 with salary above 70000"}'

# Response
{
  "success": true,
  "sql_query": "SELECT * FROM employees WHERE department = 'Engineering' AND hire_date > '2020-01-01' AND salary > 70000",
  "results": [...],
  "row_count": 15,
  "execution_time": 0.198
}
```

---

## SDK Examples

### Python SDK

```python
import requests
from typing import Dict, Any

class AgenticSQLClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def query(self, natural_query: str) -> Dict[str, Any]:
        """Execute a natural language query"""
        response = requests.post(
            f"{self.base_url}/api/query",
            json={"query": natural_query}
        )
        return response.json()
    
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema"""
        response = requests.get(f"{self.base_url}/api/schema")
        return response.json()
    
    def get_tables(self) -> list:
        """Get list of tables"""
        response = requests.get(f"{self.base_url}/api/tables")
        return response.json()["tables"]
    
    def get_history(self, limit: int = 50) -> Dict[str, Any]:
        """Get query history"""
        response = requests.get(
            f"{self.base_url}/api/history",
            params={"limit": limit}
        )
        return response.json()

# Usage
client = AgenticSQLClient()
result = client.query("Show all employees")
print(result['sql_query'])
print(result['results'])
```

### JavaScript/TypeScript SDK

```typescript
class AgenticSQLClient {
  constructor(private baseUrl: string = 'http://localhost:8000') {}
  
  async query(naturalQuery: string) {
    const response = await fetch(`${this.baseUrl}/api/query`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query: naturalQuery})
    });
    return response.json();
  }
  
  async getSchema() {
    const response = await fetch(`${this.baseUrl}/api/schema`);
    return response.json();
  }
  
  async getTables() {
    const response = await fetch(`${this.baseUrl}/api/tables`);
    const data = await response.json();
    return data.tables;
  }
  
  async getHistory(limit: number = 50) {
    const response = await fetch(
      `${this.baseUrl}/api/history?limit=${limit}`
    );
    return response.json();
  }
}

// Usage
const client = new AgenticSQLClient();
const result = await client.query('Show all employees');
console.log(result.sql_query);
console.log(result.results);
```

---

## Testing

### Test All Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Get schema
curl http://localhost:8000/api/schema

# Get tables
curl http://localhost:8000/api/tables

# Execute query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show all employees"}'

# Get history
curl http://localhost:8000/api/history?limit=10
```

### Automated Testing

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]

def test_query():
    response = requests.post(
        f"{BASE_URL}/api/query",
        json={"query": "Show all employees"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "sql_query" in data
    assert "results" in data

def test_schema():
    response = requests.get(f"{BASE_URL}/api/schema")
    assert response.status_code == 200
    data = response.json()
    assert "tables" in data
    assert len(data["tables"]) > 0
```

---

## Next Steps

- Read [DEVELOPMENT.md](DEVELOPMENT.md) for contributing
- See [CONFIGURATION.md](CONFIGURATION.md) for API customization
- Check [SETUP.md](SETUP.md) for deployment
