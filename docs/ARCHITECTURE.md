# System Architecture

## Overview

Agentic SQL follows a modern three-tier architecture with clear separation of concerns:

1. **Presentation Layer**: Next.js frontend with TypeScript
2. **Application Layer**: FastAPI backend with Python
3. **Data Layer**: SQLite/PostgreSQL database

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Query Input  │  │ Query Output │  │Schema Viewer │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│           │                  │                  │            │
│           └──────────────────┴──────────────────┘            │
│                         │ (HTTP/REST)                        │
└─────────────────────────┼────────────────────────────────────┘
                          │
┌─────────────────────────┼────────────────────────────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────┴────────────────────────────────┐  │
│  │                   API Routes                          │  │
│  │  /api/query | /api/schema | /api/history            │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────┴────────────────────────────────┐  │
│  │                   SQL Agent                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │ LLM Provider │  │Schema Intro. │  │  Executor  │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  └──────────────────────┬────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────┴────────────────────────────────┐  │
│  │              Database Connection                      │  │
│  └──────────────────────┬────────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────────┘
                          │
┌─────────────────────────┼────────────────────────────────────┐
│                    Database Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  employees   │  │  departments │  │   products   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### Frontend Components

#### 1. Header
- **Purpose**: Navigation and theme toggle
- **Features**: Dark/light mode switcher, app branding
- **State**: Theme preference (stored in localStorage)

#### 2. QueryInput
- **Purpose**: Natural language query input
- **Features**: Textarea for queries, example queries, submit button
- **Props**: `onSubmit`, `isLoading`
- **State**: Current query text

#### 3. QueryOutput
- **Purpose**: Display SQL and results
- **Features**: Syntax-highlighted SQL, formatted table results, copy buttons
- **Props**: `result` (QueryResult object)
- **State**: Copy status for clipboard operations

#### 4. SchemaViewer
- **Purpose**: Browse database schema
- **Features**: List of tables with columns and types
- **State**: Schema data from API
- **Updates**: On mount via API call

#### 5. QueryHistory
- **Purpose**: Show recent queries
- **Features**: Clickable history items, success/failure indicators
- **Props**: `onSelectQuery`
- **State**: History data, auto-refreshes every 10s

### Backend Components

#### 1. FastAPI Application (main.py)
- **Purpose**: Application entry point
- **Responsibilities**:
  - Initialize database connection
  - Create SQL Agent instance
  - Configure CORS
  - Mount API routes
  - Handle startup/shutdown events

#### 2. Configuration Loader (config.py)
- **Purpose**: Centralized configuration management
- **Features**:
  - Load YAML configuration
  - Override with environment variables
  - Provide typed settings via Pydantic
  - Support multiple LLM providers

#### 3. SQL Agent (agent/sql_agent.py)
- **Purpose**: Main orchestration logic
- **Responsibilities**:
  - Coordinate LLM, schema, and executor
  - Process natural language queries
  - Generate SQL using LLM
  - Execute queries safely
  - Return formatted results
- **Dependencies**: LLM Provider, Schema Introspector, Query Executor

#### 4. LLM Provider (agent/llm_provider.py)
- **Purpose**: Abstract LLM interactions
- **Implementations**:
  - `HuggingFaceProvider`: Local/open-source models
  - `OpenAIProvider`: OpenAI GPT models
  - `AnthropicProvider`: Claude models
- **Pattern**: Factory pattern for provider creation
- **Features**:
  - Fallback SQL generation for demo
  - Model loading with error handling
  - Prompt formatting

#### 5. Prompt Templates (agent/prompts.py)
- **Purpose**: Store LLM prompts
- **Variants**:
  - General SQL generation prompt
  - SQLCoder-specific prompt
  - OpenAI system/user prompts
  - Anthropic prompts
- **Features**: Dynamic prompt selection based on provider

#### 6. Database Connection (database/connection.py)
- **Purpose**: Manage database connections
- **Features**:
  - SQLAlchemy engine creation
  - Session management
  - Connection pooling
  - Health checks
- **Pattern**: Singleton pattern for global connection

#### 7. Schema Introspector (database/schema.py)
- **Purpose**: Inspect database structure
- **Features**:
  - Get all tables
  - Get table schemas (columns, types, constraints)
  - Generate schema context for LLM
  - Sample data retrieval
- **Uses**: SQLAlchemy inspection

#### 8. Query Executor (database/executor.py)
- **Purpose**: Safely execute SQL queries
- **Features**:
  - Query validation (prevent dangerous operations)
  - SQL injection prevention
  - Timeout handling
  - Row limiting
  - Error handling
- **Security**: Blocks write operations by default

#### 9. API Routes (api/routes.py)
- **Endpoints**:
  - `POST /api/query`: Execute natural language query
  - `GET /api/schema`: Get database schema
  - `GET /api/tables`: List tables
  - `GET /api/history`: Get query history
  - `GET /api/health`: Health check
- **Features**: Request validation, error handling, response formatting

#### 10. Pydantic Models (models/schemas.py)
- **Purpose**: Request/response validation
- **Models**:
  - `QueryRequest`: Natural language query input
  - `QueryResponse`: SQL, results, metadata
  - `SchemaResponse`: Database schema info
  - `HealthResponse`: System health status
  - `QueryHistoryResponse`: Historical queries

## Data Flow

### Query Execution Flow

```
1. User enters natural language query in frontend
   ↓
2. Frontend sends POST /api/query with query text
   ↓
3. Backend API route receives request
   ↓
4. SQL Agent processes query:
   a. Schema Introspector provides database context
   b. LLM Provider generates SQL from natural language
   c. Query Executor validates SQL
   d. Query Executor runs SQL on database
   e. Results are formatted
   ↓
5. Backend returns QueryResponse with SQL, results, metadata
   ↓
6. Frontend displays:
   - Generated SQL (syntax highlighted)
   - Results table (if successful)
   - Error message (if failed)
   - Execution time and row count
   ↓
7. Query is added to history
```

### Schema Loading Flow

```
1. Frontend mounts SchemaViewer component
   ↓
2. Component sends GET /api/schema
   ↓
3. Backend Schema Introspector inspects database
   ↓
4. Returns list of tables with columns and types
   ↓
5. Frontend displays schema in sidebar
```

## Design Decisions

### 1. Why FastAPI?
- **Reason**: High-performance async support, automatic API documentation, great developer experience
- **Alternative**: Flask - chosen FastAPI for better async and built-in validation

### 2. Why Next.js?
- **Reason**: Modern React framework, excellent DX, built-in SSR/SSG, great routing
- **Alternative**: Create React App - chosen Next.js for better performance and features

### 3. Why SQLite for Demo?
- **Reason**: Zero configuration, embedded, perfect for demos and development
- **Production**: PostgreSQL recommended for production use

### 4. Why Provider Abstraction?
- **Reason**: Allow switching between open-source and paid models without code changes
- **Pattern**: Strategy pattern for interchangeable LLM implementations

### 5. Why In-Memory History?
- **Reason**: Simple demo implementation, no additional database tables needed
- **Production**: Should use database table or Redis for persistent history

### 6. Why Schema Context Caching?
- **Reason**: Avoid repeated database introspection on every query
- **Trade-off**: Manual refresh needed if schema changes (acceptable for demo)

### 7. Why Fallback SQL Generation?
- **Reason**: Allow demo to work without downloading large LLM models
- **Production**: Should use actual LLM for production deployment

## Security Considerations

### 1. SQL Injection Prevention
- Query validation before execution
- Parameterized queries where possible
- Pattern matching for dangerous operations

### 2. Query Restrictions
- Write operations disabled by default
- Row limit enforced (max 1000 rows)
- Timeout limits (30 seconds)

### 3. CORS Configuration
- Configurable allowed origins
- Credentials support

### 4. API Keys
- Environment variables for sensitive data
- Never committed to version control

## Scalability Considerations

### Current State (Demo)
- In-memory query history
- Single-instance deployment
- SQLite database

### Production Recommendations

#### 1. Database
- Migrate to PostgreSQL
- Implement connection pooling
- Add read replicas for heavy read loads

#### 2. Caching
- Redis for query history
- Cache frequently accessed schemas
- Cache LLM responses for common queries

#### 3. Load Balancing
- Deploy multiple backend instances
- Use nginx or cloud load balancer
- Session persistence if needed

#### 4. LLM Optimization
- Use quantized models (8-bit) for memory efficiency
- Implement request queuing for expensive LLM calls
- Consider serverless GPU for on-demand inference

#### 5. Monitoring
- Add structured logging
- Implement metrics (Prometheus)
- Set up alerting for errors

## Extensibility

### Adding New Languages
1. Add language detection in frontend
2. Create language-specific prompts in `prompts.py`
3. Update LLM provider to handle multiple languages
4. Test with multilingual datasets

### Adding New Models
1. Add model configuration to `config.yaml`
2. Update provider if special handling needed
3. Create custom prompts if necessary
4. Test SQL generation quality

### Adding New Databases
1. Add connection string support in config
2. Test schema introspection
3. Verify SQL dialect compatibility
4. Update documentation

## Performance Characteristics

### Latency Breakdown

**Total Query Time**: 0.5-5 seconds (depending on model)

1. **API Request**: ~10-50ms
2. **LLM Generation**: 0.3-4s (varies by model)
   - Hugging Face local: 1-4s
   - OpenAI API: 0.5-2s
   - Anthropic API: 0.3-1.5s
3. **SQL Execution**: ~10-100ms (for demo data)
4. **Response Formatting**: ~10ms

### Bottlenecks
- LLM inference is the primary bottleneck
- Database queries are fast for demo data
- Network latency for API-based models

### Optimization Strategies
- Cache common queries
- Use faster models for simple queries
- Implement query result caching
- Pre-load models on startup
