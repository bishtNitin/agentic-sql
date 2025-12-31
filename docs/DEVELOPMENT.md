# Development Guide

Guide for developers who want to contribute to or extend Agentic SQL.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Development Setup](#development-setup)
3. [Code Style](#code-style)
4. [Adding New Features](#adding-new-features)
5. [Testing](#testing)
6. [Contributing](#contributing)

## Project Structure

```
agentic-sql/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Configuration management
│   │   ├── agent/             # LLM agent logic
│   │   │   ├── llm_provider.py   # LLM abstraction layer
│   │   │   ├── sql_agent.py      # Main agent orchestration
│   │   │   └── prompts.py        # Prompt templates
│   │   ├── database/          # Database components
│   │   │   ├── connection.py     # Connection management
│   │   │   ├── schema.py         # Schema introspection
│   │   │   └── executor.py       # Query execution
│   │   ├── api/               # API routes
│   │   │   └── routes.py         # Endpoint definitions
│   │   └── models/            # Data models
│   │       └── schemas.py        # Pydantic models
│   ├── config.yaml            # Application configuration
│   ├── requirements.txt       # Python dependencies
│   └── setup_demo_db.py       # Demo database creator
│
├── frontend/                   # Next.js frontend
│   ├── app/                   # Next.js app directory
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Main page
│   │   └── globals.css        # Global styles
│   ├── components/            # React components
│   │   ├── Header.tsx
│   │   ├── QueryInput.tsx
│   │   ├── QueryOutput.tsx
│   │   ├── SchemaViewer.tsx
│   │   ├── QueryHistory.tsx
│   │   └── ui/                # shadcn/ui components
│   └── lib/                   # Utilities
│       ├── api.ts             # API client
│       └── utils.ts           # Helper functions
│
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md
│   ├── SETUP.md
│   ├── CONFIGURATION.md
│   ├── DEVELOPMENT.md
│   └── API.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Clone and Setup

```bash
# Clone repository
git clone https://github.com/bishtNitin/agentic-sql.git
cd agentic-sql

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup_demo_db.py

# Frontend setup (new terminal)
cd frontend
npm install

# Start development servers
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## Code Style

### Python (Backend)

#### Style Guide

- Follow PEP 8
- Use type hints throughout
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes

#### Example

```python
from typing import Dict, Any, Optional

def process_query(query: str, config: Dict[str, Any]) -> Optional[str]:
    """
    Process a natural language query.
    
    Args:
        query: Natural language query string
        config: Configuration dictionary
        
    Returns:
        Generated SQL query or None if failed
        
    Raises:
        ValueError: If query is empty
    """
    if not query:
        raise ValueError("Query cannot be empty")
    
    # Implementation
    return sql_query
```

#### Linting

```bash
# Install linting tools
pip install black flake8 mypy

# Format code
black backend/app

# Check style
flake8 backend/app

# Type checking
mypy backend/app
```

### TypeScript (Frontend)

#### Style Guide

- Use TypeScript for all new code
- Follow Airbnb style guide
- Use functional components
- Use proper types, avoid `any`

#### Example

```typescript
interface QueryResult {
  success: boolean;
  sql_query?: string;
  results?: any[];
  error?: string;
}

interface QueryOutputProps {
  result: QueryResult | null;
}

export default function QueryOutput({ result }: QueryOutputProps) {
  // Implementation
}
```

#### Linting

```bash
# Install linting tools
npm install --save-dev eslint prettier

# Format code
npm run lint

# Format with Prettier
npx prettier --write "**/*.{ts,tsx}"
```

## Adding New Features

### Adding a New LLM Provider

#### Step 1: Create Provider Class

In `backend/app/agent/llm_provider.py`:

```python
class NewProvider(LLMProvider):
    """New LLM provider implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the provider"""
        # Setup logic here
        pass
    
    def generate(self, prompt: str) -> str:
        """Generate SQL from prompt"""
        # Implementation here
        pass
```

#### Step 2: Update Factory Function

```python
def create_llm_provider(config: Dict[str, Any]) -> LLMProvider:
    provider_type = config.get('provider')
    
    if provider_type == 'new_provider':
        return NewProvider(config)
    # ... existing providers
```

#### Step 3: Add Configuration

In `backend/config.yaml`:

```yaml
# New Provider Configuration
new_provider:
  api_key: your_key
  model: model_name
  temperature: 0.1
```

#### Step 4: Update Documentation

Add provider details to `docs/CONFIGURATION.md`.

### Adding a New Prompt Template

In `backend/app/agent/prompts.py`:

```python
NEW_PROVIDER_PROMPT = """
Your custom prompt template here.
Schema: {schema_context}
Question: {question}
SQL:
"""

def get_prompt_template(provider: str, model: str = None) -> str:
    if provider == "new_provider":
        return NEW_PROVIDER_PROMPT
    # ... existing logic
```

### Adding a New Frontend Component

#### Step 1: Create Component

In `frontend/components/NewComponent.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

interface NewComponentProps {
  data: any;
  onAction: (value: string) => void;
}

export default function NewComponent({ data, onAction }: NewComponentProps) {
  const [state, setState] = useState<string>('');
  
  return (
    <Card>
      <CardHeader>
        <CardTitle>New Component</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Implementation */}
      </CardContent>
    </Card>
  );
}
```

#### Step 2: Use Component

In `frontend/app/page.tsx`:

```typescript
import NewComponent from '@/components/NewComponent';

export default function Home() {
  return (
    <div>
      <NewComponent data={data} onAction={handleAction} />
    </div>
  );
}
```

### Adding Language Support (e.g., Hindi)

#### Step 1: Language Detection

In `frontend/components/QueryInput.tsx`:

```typescript
const detectLanguage = (text: string): string => {
  // Simple detection logic
  const hindiPattern = /[\u0900-\u097F]/;
  return hindiPattern.test(text) ? 'hindi' : 'english';
};
```

#### Step 2: Add Hindi Prompts

In `backend/app/agent/prompts.py`:

```python
HINDI_SQL_PROMPT = """
आप एक SQL विशेषज्ञ हैं। 
डेटाबेस स्कीमा: {schema_context}
प्रश्न: {question}
SQL क्वेरी:
"""

def get_prompt_template(provider: str, model: str = None, language: str = 'english') -> str:
    if language == 'hindi':
        return HINDI_SQL_PROMPT
    # ... existing logic
```

#### Step 3: Update API

In `backend/app/models/schemas.py`:

```python
class QueryRequest(BaseModel):
    query: str
    language: Optional[str] = 'english'
```

In `backend/app/agent/sql_agent.py`:

```python
def generate_sql(self, natural_language_query: str, language: str = 'english') -> str:
    template = get_prompt_template(provider, model, language)
    # ... rest of logic
```

### Adding a New API Endpoint

#### Step 1: Define Pydantic Model

In `backend/app/models/schemas.py`:

```python
class NewRequest(BaseModel):
    param1: str
    param2: Optional[int] = None

class NewResponse(BaseModel):
    result: str
    success: bool
```

#### Step 2: Create Route

In `backend/app/api/routes.py`:

```python
@router.post("/new-endpoint", response_model=NewResponse)
async def new_endpoint(
    request: NewRequest,
    agent: SQLAgent = Depends(get_sql_agent)
):
    """
    Description of the new endpoint
    """
    try:
        # Implementation
        result = process_request(request)
        return NewResponse(result=result, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Step 3: Update Frontend API Client

In `frontend/lib/api.ts`:

```typescript
async newEndpoint(param1: string, param2?: number) {
  const response = await this.client.post('/api/new-endpoint', {
    param1,
    param2
  });
  return response.data;
}
```

## Testing

### Backend Testing

#### Unit Tests

Create `backend/tests/test_agent.py`:

```python
import pytest
from app.agent.sql_agent import SQLAgent
from app.config import config

def test_sql_generation():
    """Test SQL generation from natural language"""
    agent = SQLAgent(
        llm_config=config.get_provider_config(),
        engine=get_test_engine(),
        execution_config=config.get_execution_config()
    )
    
    query = "Show all employees"
    sql = agent.generate_sql(query)
    
    assert "SELECT" in sql.upper()
    assert "employees" in sql.lower()

def test_query_execution():
    """Test query execution"""
    agent = SQLAgent(...)
    result = agent.process_query("Show all employees")
    
    assert result['success'] is True
    assert 'results' in result
    assert len(result['results']) > 0
```

#### Run Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests
pytest backend/tests

# With coverage
pytest --cov=backend/app backend/tests
```

### Frontend Testing

#### Component Tests

Create `frontend/__tests__/QueryInput.test.tsx`:

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import QueryInput from '@/components/QueryInput';

describe('QueryInput', () => {
  it('renders input textarea', () => {
    render(<QueryInput onSubmit={jest.fn()} isLoading={false} />);
    const textarea = screen.getByPlaceholderText(/ask a question/i);
    expect(textarea).toBeInTheDocument();
  });
  
  it('calls onSubmit when form is submitted', () => {
    const onSubmit = jest.fn();
    render(<QueryInput onSubmit={onSubmit} isLoading={false} />);
    
    const textarea = screen.getByRole('textbox');
    const button = screen.getByText(/execute/i);
    
    fireEvent.change(textarea, { target: { value: 'Test query' } });
    fireEvent.click(button);
    
    expect(onSubmit).toHaveBeenCalledWith('Test query');
  });
});
```

#### Run Tests

```bash
# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

### Integration Tests

Create `tests/integration/test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

def test_full_query_flow():
    """Test complete query flow"""
    # Execute query
    response = requests.post(
        f"{BASE_URL}/api/query",
        json={"query": "Show all employees"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['success'] is True
    
    # Check history
    response = requests.get(f"{BASE_URL}/api/history")
    history = response.json()
    assert len(history['history']) > 0
```

## Contributing

### Contribution Workflow

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone
   git clone https://github.com/YOUR_USERNAME/agentic-sql.git
   cd agentic-sql
   git remote add upstream https://github.com/bishtNitin/agentic-sql.git
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write code following style guides
   - Add tests for new features
   - Update documentation

4. **Test Changes**
   ```bash
   # Backend tests
   pytest backend/tests
   
   # Frontend tests
   npm test
   
   # Manual testing
   # Start servers and test functionality
   ```

5. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```
   
   Use conventional commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `style:` Code style
   - `refactor:` Refactoring
   - `test:` Tests
   - `chore:` Maintenance

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then create a Pull Request on GitHub.

### Pull Request Guidelines

- Clear description of changes
- Reference related issues
- Include tests
- Update documentation
- Ensure CI passes
- Follow code style

### Code Review Process

1. Automated checks (linting, tests)
2. Manual code review
3. Address feedback
4. Approval and merge

## Best Practices

### Backend

1. **Type Hints**: Always use type hints
   ```python
   def function(arg: str) -> Dict[str, Any]:
       ...
   ```

2. **Error Handling**: Catch specific exceptions
   ```python
   try:
       result = operation()
   except SpecificError as e:
       logger.error(f"Operation failed: {e}")
       raise
   ```

3. **Logging**: Use structured logging
   ```python
   logger.info(f"Processing query: {query}", extra={
       "query_length": len(query),
       "user_id": user_id
   })
   ```

4. **Configuration**: Use environment variables for secrets
   ```python
   api_key = os.getenv("API_KEY")
   if not api_key:
       raise ValueError("API_KEY not set")
   ```

### Frontend

1. **Component Organization**: Keep components small and focused

2. **State Management**: Use appropriate hooks
   ```typescript
   const [data, setData] = useState<DataType | null>(null);
   const [loading, setLoading] = useState(false);
   ```

3. **Error Boundaries**: Wrap components in error boundaries

4. **Accessibility**: Use semantic HTML and ARIA labels

## Debugging

### Backend Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for interactive debugging
import pdb; pdb.set_trace()

# Or use ipdb
import ipdb; ipdb.set_trace()
```

### Frontend Debugging

```typescript
// Console logging
console.log('Data:', data);
console.error('Error:', error);

// React DevTools
// Install browser extension

// Network debugging
// Use browser DevTools Network tab
```

## Performance Optimization

### Backend

1. **Caching**: Cache schema and frequent queries
2. **Connection Pooling**: Use proper pool size
3. **Async Operations**: Use async/await for I/O
4. **Query Optimization**: Add indexes, limit results

### Frontend

1. **Code Splitting**: Use dynamic imports
2. **Memoization**: Use React.memo, useMemo
3. **Lazy Loading**: Load components on demand
4. **Image Optimization**: Use Next.js Image component

## Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **TypeScript**: https://www.typescriptlang.org/docs/

## Getting Help

- GitHub Issues: Bug reports and feature requests
- Discussions: Questions and community support
- Documentation: Check all docs/ files first

## License

MIT License - see LICENSE file for details.
