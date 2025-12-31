# End-to-End Workflow Guide

## 🔄 Complete Project Workflow

This document provides a comprehensive walkthrough of the Agentic SQL project from start to finish, including the request flow, data processing, and component interactions.

---

## 📋 Table of Contents

1. [Project Initialization](#1-project-initialization)
2. [System Startup](#2-system-startup)
3. [User Request Flow](#3-user-request-flow)
4. [SQL Generation Process](#4-sql-generation-process)
5. [Query Execution Flow](#5-query-execution-flow)
6. [Response Flow](#6-response-flow)
7. [Component Interactions](#7-component-interactions)

---

## 1. Project Initialization

### Step 1.1: Clone and Setup

```bash
# Clone repository
git clone https://github.com/bishtNitin/agentic-sql.git
cd agentic-sql

# Copy environment configuration
cp .env.example .env
```

**What happens:**
- Repository is cloned to local machine
- Environment template is copied for configuration

### Step 1.2: Configuration

Edit `.env` file to configure:
```bash
DATABASE_URL=sqlite:///./demo.db
LLM_PROVIDER=huggingface  # or openai, anthropic
HUGGINGFACE_MODEL=defog/sqlcoder-7b-2
```

**Configuration priority:**
1. Environment variables (`.env`)
2. YAML configuration (`backend/config.yaml`)
3. Default values (in code)

### Step 1.3: Database Setup

```bash
cd backend
python setup_demo_db.py
```

**What happens:**
1. Script creates `demo.db` SQLite database
2. Creates 5 tables:
   - `employees` (50 rows)
   - `departments` (5 rows)
   - `products` (15 rows)
   - `customers` (30 rows)
   - `orders` (100 rows)
3. Populates with sample data
4. Establishes foreign key relationships

**Database Schema Created:**
```
employees: id, name, department, salary, hire_date
departments: id, name, budget, manager_id
products: id, name, category, price, stock
customers: id, name, email, city, registration_date
orders: id, product_id, customer_name, quantity, order_date
```

---

## 2. System Startup

### Step 2.1: Backend Initialization

```bash
# Option A: Quick start script
./start.sh

# Option B: Manual backend start
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend Startup Sequence:**

```
1. Load Configuration
   ├── Read config.yaml
   ├── Load environment variables
   └── Merge configurations

2. Initialize Database Connection
   ├── Create SQLAlchemy engine
   ├── Test connection (SELECT 1)
   └── Set up connection pool

3. Initialize LLM Provider
   ├── Detect provider type (huggingface/openai/anthropic)
   ├── Load model or API client
   │   ├── HuggingFace: Attempt to load transformers model
   │   ├── OpenAI: Initialize API client with key
   │   └── Anthropic: Initialize API client with key
   └── Fallback to demo mode if loading fails

4. Create SQL Agent
   ├── Instantiate with LLM provider
   ├── Create Schema Introspector
   ├── Create Query Executor
   └── Cache database schema context

5. Start FastAPI Server
   ├── Mount API routes
   ├── Configure CORS
   ├── Enable Swagger docs (/docs)
   └── Listen on port 8000
```

**Console Output:**
```
INFO: Starting Agentic SQL API...
INFO: Connecting to database: sqlite:///./demo.db
INFO: Database connection established
INFO: Initializing SQL Agent with provider: huggingface
WARNING: Transformers library not installed: No module named 'transformers'
WARNING: Using mock provider for demo
INFO: SQL Agent initialized successfully
INFO: Agentic SQL API is ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 2.2: Frontend Initialization

```bash
# New terminal
cd frontend
npm install
npm run dev
```

**Frontend Startup Sequence:**

```
1. Load Next.js Application
   ├── Initialize React runtime
   ├── Load Tailwind CSS
   └── Set up client-side routing

2. Initialize Components
   ├── Header (with theme detection)
   ├── QueryInput (with example queries)
   ├── QueryOutput (placeholder state)
   ├── SchemaViewer (loading state)
   └── QueryHistory (empty state)

3. Fetch Initial Data
   ├── GET /api/schema (background)
   ├── GET /api/history (background)
   └── Update UI with loaded data

4. Start Development Server
   └── Listen on port 3000
```

**Browser Output:**
```
Application ready at http://localhost:3000
```

---

## 3. User Request Flow

### Step 3.1: User Types Query

**User Action:**
```
User types in QueryInput: "Show all employees with salary greater than 60000"
```

**Frontend State:**
```typescript
// QueryInput component
const [query, setQuery] = useState('Show all employees with salary greater than 60000');
const [isLoading, setIsLoading] = useState(false);
```

### Step 3.2: Form Submission

**User clicks "Execute Query" button**

**Frontend Flow:**
```typescript
// 1. Validate input
if (!query.trim()) return;

// 2. Set loading state
setIsLoading(true);

// 3. Make API call
const response = await apiClient.executeQuery(query);

// 4. Update state with results
setResult(response);
setIsLoading(false);
```

### Step 3.3: HTTP Request

**API Client sends POST request:**

```http
POST http://localhost:8000/api/query
Content-Type: application/json

{
  "query": "Show all employees with salary greater than 60000"
}
```

---

## 4. SQL Generation Process

### Step 4.1: Request Reception

**Backend receives request at `/api/query` endpoint:**

```python
# api/routes.py
@router.post("/api/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest, agent: SQLAgent = Depends(get_sql_agent)):
    # 1. Log request
    logger.info(f"Received query: {request.query}")
    
    # 2. Process with SQL Agent
    result = agent.process_query(request.query)
    
    # 3. Store in history
    # 4. Return response
```

### Step 4.2: SQL Agent Processing

**SQL Agent orchestrates the generation:**

```python
# agent/sql_agent.py
def process_query(self, natural_language_query: str) -> Dict[str, Any]:
    # Step 1: Generate SQL from natural language
    sql_query = self.generate_sql(natural_language_query)
    
    # Step 2: Execute the SQL
    result = self.query_executor.execute(sql_query)
    
    return result
```

### Step 4.3: Schema Context Preparation

**Schema Introspector provides context:**

```python
# database/schema.py
def get_schema_context(self) -> str:
    """
    Returns formatted schema:
    
    Database Schema:
    
    Table: employees
      - id (INTEGER, NOT NULL) PRIMARY KEY
      - name (VARCHAR(100), NOT NULL)
      - department (VARCHAR(50), NULL)
      - salary (INTEGER, NULL)
      - hire_date (DATE, NULL)
    
    Table: departments
      - id (INTEGER, NOT NULL) PRIMARY KEY
      - name (VARCHAR(50), NOT NULL)
      - budget (INTEGER, NULL)
      - manager_id (INTEGER, NULL)
    """
```

### Step 4.4: Prompt Construction

**Prompt template is filled with context:**

```python
# agent/prompts.py
SQL_GENERATION_PROMPT = """
You are an expert SQL query generator.

{schema_context}

Important Instructions:
1. Generate ONLY the SQL query
2. Use proper SQL syntax
3. Match table/column names exactly

Natural Language: {question}
SQL:
"""

# Formatted prompt
prompt = """
You are an expert SQL query generator.

Database Schema:

Table: employees
  - id (INTEGER, NOT NULL) PRIMARY KEY
  - name (VARCHAR(100), NOT NULL)
  - salary (INTEGER, NULL)
  ...

Natural Language: Show all employees with salary greater than 60000
SQL:
"""
```

### Step 4.5: LLM Generation

**Two paths depending on setup:**

#### Path A: Actual LLM (if installed)
```python
# agent/llm_provider.py - HuggingFaceProvider
def generate(self, prompt: str) -> str:
    # 1. Tokenize input
    inputs = self.tokenizer(prompt, return_tensors="pt")
    
    # 2. Generate with model
    outputs = self.model.generate(
        **inputs,
        max_length=512,
        temperature=0.1,
        top_p=0.95
    )
    
    # 3. Decode output
    generated_text = self.tokenizer.decode(outputs[0])
    
    # 4. Extract SQL
    sql_query = self._extract_sql(generated_text, prompt)
    
    return sql_query
```

**Output:** `"SELECT * FROM employees WHERE salary > 60000"`

#### Path B: Fallback Mode (demo without ML dependencies)
```python
# agent/llm_provider.py - HuggingFaceProvider._fallback_generate
def _fallback_generate(self, prompt: str) -> str:
    question_lower = prompt.lower()
    
    # Pattern matching for common queries
    if "salary" in question_lower and ">" in question_lower:
        numbers = re.findall(r'\d+', question_lower)
        if numbers:
            return f"SELECT * FROM employees WHERE salary > {numbers[0]}"
    
    # ... more patterns
```

**Output:** `"SELECT * FROM employees WHERE salary > 60000"`

### Step 4.6: SQL Cleaning

**Generated SQL is cleaned:**

```python
# agent/sql_agent.py
def _clean_sql(self, sql: str) -> str:
    # Remove markdown
    sql = sql.replace("```sql", "").replace("```", "")
    
    # Remove whitespace
    sql = sql.strip()
    
    # Remove trailing semicolon
    if sql.endswith(';'):
        sql = sql[:-1].strip()
    
    return sql
```

**Result:** `"SELECT * FROM employees WHERE salary > 60000"`

---

## 5. Query Execution Flow

### Step 5.1: Query Validation

**Query Executor validates safety:**

```python
# database/executor.py
def validate_query(self, query: str) -> Tuple[bool, str]:
    # 1. Check for empty query
    if not query.strip():
        return False, "Empty query"
    
    # 2. Check for dangerous operations (if write disabled)
    if not self.enable_write_queries:
        dangerous = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE']
        for keyword in dangerous:
            if query.upper().startswith(keyword):
                return False, f"Write operations disabled"
    
    # 3. Check for SQL injection patterns
    injection_patterns = [r';\s*DROP', r';\s*DELETE', ...]
    
    return True, ""
```

**Validation Result:** `(True, "")`

### Step 5.2: SQL Execution

**Query is executed on database:**

```python
# database/executor.py
def execute(self, query: str) -> Dict[str, Any]:
    start_time = time.time()
    
    # 1. Validate
    is_valid, error = self.validate_query(query)
    
    # 2. Execute with SQLAlchemy
    with self.engine.connect() as conn:
        result = conn.execute(text(query))
        
        # 3. Fetch results
        if query.upper().startswith('SELECT'):
            columns = list(result.keys())
            rows = result.fetchall()
            
            # 4. Limit rows
            limited_rows = rows[:self.max_rows]  # max 1000
            
            # 5. Convert to dictionaries
            results = [dict(zip(columns, row)) for row in limited_rows]
    
    execution_time = time.time() - start_time
    
    return {
        'success': True,
        'sql_query': query,
        'results': results,
        'columns': columns,
        'row_count': len(results),
        'execution_time': round(execution_time, 3)
    }
```

**Execution Result:**
```python
{
    'success': True,
    'sql_query': 'SELECT * FROM employees WHERE salary > 60000',
    'results': [
        {'id': 2, 'name': 'David Garcia', 'department': 'Finance', 'salary': 91999, 'hire_date': '2024-12-31'},
        {'id': 3, 'name': 'John Davis', 'department': 'Marketing', 'salary': 92464, 'hire_date': '2025-08-18'},
        {'id': 4, 'name': 'Richard Williams', 'department': 'Human Resources', 'salary': 122359, 'hire_date': '2024-02-10'},
        # ... more rows
    ],
    'columns': ['id', 'name', 'department', 'salary', 'hire_date'],
    'row_count': 28,
    'execution_time': 0.145
}
```

### Step 5.3: History Storage

**Query is saved to history:**

```python
# api/routes.py
history_item = {
    'id': len(query_history) + 1,
    'natural_query': request.query,
    'sql_query': result.get('sql_query', ''),
    'success': result.get('success', False),
    'timestamp': datetime.now()
}
query_history.append(history_item)
```

---

## 6. Response Flow

### Step 6.1: HTTP Response

**Backend sends JSON response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "sql_query": "SELECT * FROM employees WHERE salary > 60000",
  "results": [
    {
      "id": 2,
      "name": "David Garcia",
      "department": "Finance",
      "salary": 91999,
      "hire_date": "2024-12-31"
    },
    ...
  ],
  "columns": ["id", "name", "department", "salary", "hire_date"],
  "row_count": 28,
  "execution_time": 0.145,
  "error": null
}
```

### Step 6.2: Frontend Processing

**React component updates:**

```typescript
// app/page.tsx
const handleQuerySubmit = async (query: string) => {
    setIsLoading(true);
    
    try {
        // API call returns
        const data = await apiClient.executeQuery(query);
        
        // Update result state
        setResult(data);
        
    } catch (error) {
        setResult({
            success: false,
            error: error.message
        });
    } finally {
        setIsLoading(false);
    }
};
```

### Step 6.3: UI Rendering

**QueryOutput component displays results:**

```typescript
// components/QueryOutput.tsx
export default function QueryOutput({ result }) {
    if (!result) {
        // Show placeholder
        return <Database icon with "Results will appear here" />;
    }
    
    return (
        <Card>
            {/* Success indicator */}
            <CheckCircle /> Query Successful
            
            {/* Execution time */}
            <Clock /> 0.145s
            
            {/* Generated SQL with syntax highlighting */}
            <SyntaxHighlighter language="sql">
                {result.sql_query}
            </SyntaxHighlighter>
            
            {/* Results table */}
            <table>
                <thead>
                    {result.columns.map(col => <th>{col}</th>)}
                </thead>
                <tbody>
                    {result.results.map(row => (
                        <tr>
                            {result.columns.map(col => (
                                <td>{row[col]}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
            
            {/* Row count */}
            28 rows returned
        </Card>
    );
}
```

**User sees:**
- ✅ Query Successful badge
- ⏱️ Execution time: 0.145s
- 💻 Syntax-highlighted SQL query
- 📊 Results table with 28 rows
- 📋 Copy button to clipboard

### Step 6.4: Background Updates

**Other components refresh:**

```typescript
// components/QueryHistory.tsx
useEffect(() => {
    // Refresh history every 10 seconds
    const interval = setInterval(loadHistory, 10000);
    return () => clearInterval(interval);
}, []);

// After query execution, history updates show:
// ✅ "Show all employees with salary greater than 60000"
//    SELECT * FROM employees WHERE salary > 60000
```

---

## 7. Component Interactions

### Complete Request-Response Cycle Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Frontend (React/Next.js) - http://localhost:3000         │  │
│  │                                                           │  │
│  │  1. User types: "Show employees with salary > 60000"     │  │
│  │  2. Clicks "Execute Query"                               │  │
│  │  3. QueryInput validates & sends request                 │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTP POST /api/query
                         │ {"query": "Show..."}
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND SERVER                               │
│            FastAPI - http://localhost:8000                      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. API Routes (routes.py)                                │  │
│  │    - Receives request                                    │  │
│  │    - Validates with Pydantic                             │  │
│  │    - Calls SQL Agent                                     │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼──────────────────────────────────────┐  │
│  │ 2. SQL Agent (sql_agent.py)                              │  │
│  │    - Orchestrates the process                            │  │
│  │    - Calls schema introspector                           │  │
│  │    - Prepares prompt                                     │  │
│  │    - Calls LLM provider                                  │  │
│  └────────┬──────────────────────────┬──────────────────────┘  │
│           │                          │                          │
│  ┌────────▼──────────────┐  ┌────────▼──────────────┐          │
│  │ 3a. Schema            │  │ 3b. LLM Provider      │          │
│  │     Introspector      │  │     (llm_provider.py) │          │
│  │     (schema.py)       │  │                       │          │
│  │                       │  │  - Uses prompt        │          │
│  │  - Gets all tables    │  │  - Generates SQL      │          │
│  │  - Gets columns       │  │    (fallback mode)    │          │
│  │  - Formats context    │  │                       │          │
│  │                       │  │  Result:              │          │
│  │  Result:              │  │  "SELECT * FROM       │          │
│  │  "Table: employees    │  │   employees WHERE     │          │
│  │   - id (INTEGER)..."  │  │   salary > 60000"     │          │
│  └───────────────────────┘  └───────────────────────┘          │
│                       │                                          │
│  ┌────────────────────▼──────────────────────────────────────┐  │
│  │ 4. Query Executor (executor.py)                          │  │
│  │    - Validates SQL (no DROP/DELETE/etc.)                 │  │
│  │    - Checks for SQL injection                            │  │
│  │    - Executes on database                                │  │
│  │    - Limits rows to 1000                                 │  │
│  │    - Formats results                                     │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼──────────────────────────────────────┐  │
│  │ 5. Database (SQLite)                                     │  │
│  │    - Executes: SELECT * FROM employees WHERE salary>60000│  │
│  │    - Returns 28 rows                                     │  │
│  │    - Execution time: 0.145s                              │  │
│  └────────────────────┬──────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼──────────────────────────────────────┐  │
│  │ 6. Format Response                                       │  │
│  │    {                                                     │  │
│  │      "success": true,                                    │  │
│  │      "sql_query": "SELECT...",                           │  │
│  │      "results": [{...}, {...}],                          │  │
│  │      "columns": ["id", "name"...],                       │  │
│  │      "row_count": 28,                                    │  │
│  │      "execution_time": 0.145                             │  │
│  │    }                                                     │  │
│  └────────────────────┬──────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTP 200 OK
                         │ JSON Response
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Frontend Receives Response                               │  │
│  │                                                           │  │
│  │  7. QueryOutput updates:                                 │  │
│  │     - Shows success indicator                            │  │
│  │     - Displays SQL with syntax highlighting              │  │
│  │     - Renders results table                              │  │
│  │     - Shows execution time                               │  │
│  │                                                           │  │
│  │  8. QueryHistory refreshes:                              │  │
│  │     - Adds new query to history                          │  │
│  │     - Shows in sidebar                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Timing Breakdown

```
Total Request Time: ~200-500ms

├─ Frontend Processing: ~10ms
│  └─ React state update, validation
│
├─ Network (Request): ~5-10ms
│  └─ HTTP POST to backend
│
├─ Backend Processing: ~150-400ms
│  ├─ Request parsing: ~2ms
│  ├─ Schema introspection (cached): ~5ms
│  ├─ LLM generation: ~50-300ms
│  │  ├─ Fallback mode: ~50ms (pattern matching)
│  │  └─ Actual LLM: ~300-4000ms (model-dependent)
│  ├─ SQL validation: ~2ms
│  ├─ Query execution: ~10-100ms
│  └─ Response formatting: ~2ms
│
├─ Network (Response): ~5-10ms
│  └─ JSON response to frontend
│
└─ Frontend Rendering: ~20-50ms
   └─ React component re-render, table display
```

---

## 8. Additional Workflows

### Schema Browsing Flow

```
User opens application
    ↓
SchemaViewer component mounts
    ↓
GET /api/schema
    ↓
Backend: Schema Introspector gets all tables
    ↓
Returns: [{table_name: "employees", columns: [...]}]
    ↓
Frontend displays in sidebar
```

### Query History Flow

```
After each query execution
    ↓
Backend stores in memory: query_history.append({...})
    ↓
Frontend polls every 10 seconds: GET /api/history
    ↓
Backend returns last 50 items
    ↓
Frontend updates QueryHistory component
    ↓
User clicks history item → Pre-fills QueryInput
```

### Theme Toggle Flow

```
User clicks moon/sun icon
    ↓
Header component: toggleTheme()
    ↓
localStorage.setItem('theme', newTheme)
    ↓
document.documentElement.classList.toggle('dark')
    ↓
CSS variables update globally
    ↓
All components re-render with new theme
```

---

## 9. Error Handling Workflows

### SQL Generation Error

```
User: "Show me xyz from invalid_table"
    ↓
LLM generates: "SELECT * FROM invalid_table"
    ↓
Executor validates (passes)
    ↓
Database execution fails: "no such table"
    ↓
Executor catches exception
    ↓
Returns: {success: false, error: "no such table: invalid_table"}
    ↓
Frontend shows error message in red box
```

### Dangerous Query Blocked

```
User: "Delete all employees"
    ↓
LLM generates: "DELETE FROM employees"
    ↓
Executor validates
    ↓
Detects: query starts with "DELETE"
    ↓
Validation fails: "Write operations are disabled"
    ↓
Returns: {success: false, error: "Write operations disabled"}
    ↓
Query never reaches database
    ↓
Frontend shows error message
```

---

## 10. Key Takeaways

### Request Flow Summary
1. **User Input** → Frontend validation
2. **HTTP Request** → Backend API
3. **SQL Agent** → Orchestrates process
4. **Schema + LLM** → Generate SQL
5. **Executor** → Validate and execute
6. **Database** → Return results
7. **HTTP Response** → Back to frontend
8. **UI Update** → Display results

### Component Responsibilities
- **Frontend**: User interface, input validation, result display
- **API Routes**: Request handling, response formatting
- **SQL Agent**: Orchestration, workflow management
- **LLM Provider**: Natural language to SQL conversion
- **Schema Introspector**: Database structure information
- **Query Executor**: Safe SQL execution
- **Database**: Data storage and retrieval

### Safety Measures
- ✅ Query validation before execution
- ✅ SQL injection pattern detection
- ✅ Write operation blocking
- ✅ Row count limiting (max 1000)
- ✅ Execution timeout (30 seconds)
- ✅ Error handling at every level

### Performance Optimization
- 🚀 Schema caching (avoid repeated introspection)
- 🚀 Connection pooling (reuse database connections)
- 🚀 Async API (non-blocking operations)
- 🚀 Frontend memoization (avoid unnecessary re-renders)

---

This workflow ensures safe, efficient, and user-friendly natural language database querying!
