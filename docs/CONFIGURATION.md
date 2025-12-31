# Configuration Guide

This guide explains how to configure Agentic SQL for different LLM providers and use cases.

## Configuration Files

### 1. `backend/config.yaml`

Main configuration file for the application.

### 2. `.env`

Environment variables that override config.yaml settings.

## LLM Provider Configuration

### Supported Providers

1. **Hugging Face** (Open-source, free)
2. **OpenAI** (Paid API)
3. **Anthropic** (Paid API)

### Switching Providers

Edit `backend/config.yaml` to change the provider:

```yaml
# Set the provider
provider: huggingface  # Options: huggingface, openai, anthropic
```

## Hugging Face Configuration

### Default Setup (Free, No API Key)

```yaml
provider: huggingface

huggingface:
  default_model: defog/sqlcoder-7b-2
  max_length: 512
  temperature: 0.1
  top_p: 0.95
  device: cpu
  load_in_8bit: false
```

### Available Models

#### SQLCoder (Recommended for SQL)
```yaml
default_model: defog/sqlcoder-7b-2
# Best for SQL generation
# Size: ~14 GB
# RAM required: 16 GB (8 GB with 8-bit quantization)
```

#### CodeLlama
```yaml
default_model: codellama/CodeLlama-7b-Instruct-hf
# Good for code generation including SQL
# Size: ~13 GB
# RAM required: 16 GB
```

#### Mistral
```yaml
default_model: mistralai/Mistral-7B-Instruct-v0.2
# General purpose, decent for SQL
# Size: ~14 GB
# RAM required: 16 GB
```

### Memory Optimization

For systems with limited RAM (8 GB):

```yaml
huggingface:
  default_model: defog/sqlcoder-7b-2
  device: cpu
  load_in_8bit: true  # Reduces memory usage by ~50%
```

For systems with CUDA GPU:

```yaml
huggingface:
  default_model: defog/sqlcoder-7b-2
  device: cuda
  load_in_8bit: false
```

### Model Parameters

```yaml
huggingface:
  max_length: 512
  # Maximum tokens to generate
  # Higher = longer SQL queries, but slower
  # Range: 256-1024

  temperature: 0.1
  # Randomness in generation
  # Lower = more deterministic
  # Range: 0.0-1.0
  # Recommended: 0.1 for SQL

  top_p: 0.95
  # Nucleus sampling threshold
  # Higher = more diverse outputs
  # Range: 0.0-1.0
  # Recommended: 0.95 for SQL
```

## OpenAI Configuration

### Setup

1. Get API key from https://platform.openai.com/api-keys

2. Update `backend/config.yaml`:

```yaml
provider: openai

openai:
  model: gpt-4
  temperature: 0.1
  max_tokens: 500
```

3. Set environment variable in `.env`:

```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
```

### Available Models

#### GPT-4 (Best Quality)
```yaml
model: gpt-4
# Most capable, best for complex queries
# Cost: $0.03 per 1K input tokens, $0.06 per 1K output tokens
```

#### GPT-4 Turbo
```yaml
model: gpt-4-turbo-preview
# Faster than GPT-4, still high quality
# Cost: $0.01 per 1K input tokens, $0.03 per 1K output tokens
```

#### GPT-3.5 Turbo (Fastest, Cheapest)
```yaml
model: gpt-3.5-turbo
# Fast and affordable, good for simple queries
# Cost: $0.0005 per 1K input tokens, $0.0015 per 1K output tokens
```

### Parameters

```yaml
openai:
  temperature: 0.1
  # Lower = more consistent SQL
  # Range: 0.0-2.0

  max_tokens: 500
  # Maximum length of SQL query
  # Range: 1-4096
```

## Anthropic Configuration

### Setup

1. Get API key from https://console.anthropic.com/

2. Update `backend/config.yaml`:

```yaml
provider: anthropic

anthropic:
  model: claude-3-sonnet-20240229
  temperature: 0.1
  max_tokens: 500
```

3. Set environment variable in `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### Available Models

#### Claude 3 Opus (Best Quality)
```yaml
model: claude-3-opus-20240229
# Most capable, best reasoning
# Cost: $15 per 1M input tokens, $75 per 1M output tokens
```

#### Claude 3 Sonnet (Balanced)
```yaml
model: claude-3-sonnet-20240229
# Good balance of speed and quality
# Cost: $3 per 1M input tokens, $15 per 1M output tokens
```

#### Claude 3 Haiku (Fastest)
```yaml
model: claude-3-haiku-20240307
# Fast and affordable
# Cost: $0.25 per 1M input tokens, $1.25 per 1M output tokens
```

## Database Configuration

### SQLite (Default)

```yaml
database:
  type: sqlite
  path: ./demo.db
```

Or via environment variable:

```bash
DATABASE_URL=sqlite:///./demo.db
```

### PostgreSQL

```yaml
database:
  type: postgresql
  host: localhost
  port: 5432
  database: agentic_sql
  username: postgres
  password: password
```

Or via environment variable (recommended):

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Connection Pooling (PostgreSQL)

For production PostgreSQL:

```python
# In backend/app/database/connection.py
engine = create_engine(
    database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

## Query Execution Settings

```yaml
execution:
  timeout: 30
  # Query execution timeout in seconds
  # Prevents long-running queries

  max_rows: 1000
  # Maximum rows to return
  # Prevents memory issues with large results

  enable_write_queries: false
  # Allow INSERT/UPDATE/DELETE operations
  # Set to true for production if needed
  # WARNING: Be cautious with this setting
```

## Logging Configuration

```yaml
logging:
  level: INFO
  # Options: DEBUG, INFO, WARNING, ERROR
  # DEBUG: Detailed logs for development
  # INFO: Normal operation logs
  # WARNING: Only warnings and errors
  # ERROR: Only errors

  format: json
  # Options: json, text
  # json: Structured logs for production
  # text: Human-readable logs for development
```

## CORS Configuration

Configure allowed origins for frontend:

```bash
# In .env
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://yourdomain.com
```

Multiple origins separated by commas.

## Environment Variables Reference

### Required Variables

```bash
# Database
DATABASE_URL=sqlite:///./demo.db

# LLM Provider
LLM_PROVIDER=huggingface
```

### Optional Variables

```bash
# Hugging Face
HUGGINGFACE_MODEL=defog/sqlcoder-7b-2

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000
```

## Configuration Priority

Configuration values are resolved in this order (highest priority first):

1. Environment variables (.env)
2. YAML configuration (config.yaml)
3. Default values (in code)

Example:
```yaml
# config.yaml
huggingface:
  default_model: defog/sqlcoder-7b-2
```

```bash
# .env (overrides config.yaml)
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

Result: Uses Mistral model from .env

## Production Configuration Examples

### Example 1: High-Performance Setup

```yaml
# config.yaml
provider: openai

openai:
  model: gpt-3.5-turbo
  temperature: 0.1
  max_tokens: 300

execution:
  timeout: 15
  max_rows: 500
  enable_write_queries: false

logging:
  level: WARNING
  format: json
```

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/prod_db
OPENAI_API_KEY=sk-...
CORS_ORIGINS=https://app.yourdomain.com
```

### Example 2: Cost-Optimized Setup

```yaml
# config.yaml
provider: huggingface

huggingface:
  default_model: defog/sqlcoder-7b-2
  load_in_8bit: true
  device: cpu
  temperature: 0.1

execution:
  timeout: 30
  max_rows: 1000
  enable_write_queries: false
```

### Example 3: High-Accuracy Setup

```yaml
# config.yaml
provider: anthropic

anthropic:
  model: claude-3-opus-20240229
  temperature: 0.0  # Maximum determinism
  max_tokens: 1000

execution:
  timeout: 60
  max_rows: 5000
  enable_write_queries: false
```

## Testing Configuration

### Test with Different Models

```bash
# Terminal 1: Test Hugging Face
export LLM_PROVIDER=huggingface
uvicorn app.main:app --reload

# Terminal 2: Test OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
uvicorn app.main:app --reload --port 8001

# Terminal 3: Test Anthropic
export LLM_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn app.main:app --reload --port 8002
```

### Verify Configuration

```bash
# Check active configuration
curl http://localhost:8000/api/health

# Response includes current provider
{
  "status": "healthy",
  "llm_provider": "huggingface",
  ...
}
```

## Troubleshooting

### Issue: Model Not Found

**Solution**: Check model name spelling in config:
```yaml
huggingface:
  default_model: defog/sqlcoder-7b-2  # Correct
  # default_model: defog/sqlcoder7b2  # Wrong
```

### Issue: Out of Memory

**Solution**: Enable 8-bit quantization:
```yaml
huggingface:
  load_in_8bit: true
```

### Issue: API Key Invalid

**Solution**: Verify API key:
```bash
# Test OpenAI key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test Anthropic key
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

### Issue: Slow Response Time

**Solutions**:
1. Use faster model (GPT-3.5, Claude Haiku)
2. Reduce max_tokens/max_length
3. Use GPU for Hugging Face models
4. Implement caching

## Best Practices

### Development
- Use SQLite database
- Use Hugging Face with fallback mode
- Set logging level to DEBUG
- Enable CORS for localhost

### Production
- Use PostgreSQL database
- Use paid API (OpenAI/Anthropic) for reliability
- Set logging level to WARNING or ERROR
- Configure specific CORS origins
- Enable SSL/TLS
- Set appropriate timeouts
- Monitor API usage and costs

### Security
- Never commit API keys to git
- Use environment variables for secrets
- Restrict CORS origins
- Keep write queries disabled unless needed
- Implement rate limiting
- Use strong database passwords

## Next Steps

After configuring:

1. Test the configuration with health check
2. Try example queries
3. Monitor performance and costs
4. Adjust parameters based on results
5. Read [DEVELOPMENT.md](DEVELOPMENT.md) for customization
