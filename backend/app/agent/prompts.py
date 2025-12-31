"""
Prompt templates for SQL generation
"""

SQL_GENERATION_PROMPT = """You are an expert SQL query generator. Your task is to convert natural language questions into valid SQL queries.

{schema_context}

Important Instructions:
1. Generate ONLY the SQL query without any explanation or markdown formatting
2. Do NOT include triple backticks, "sql", or any other text
3. Use proper SQL syntax for the given database schema
4. Return only SELECT queries unless specifically asked for modifications
5. Use appropriate JOINs when querying multiple tables
6. Use proper WHERE clauses for filtering
7. Use aggregate functions (COUNT, SUM, AVG, etc.) when appropriate
8. Ensure column names and table names match exactly with the schema

Examples:
Natural Language: "Show all employees"
SQL: SELECT * FROM employees

Natural Language: "Find employees earning more than 50000"
SQL: SELECT * FROM employees WHERE salary > 50000

Natural Language: "Count employees by department"
SQL: SELECT department, COUNT(*) as employee_count FROM employees GROUP BY department

Natural Language: "Show top 5 products by price"
SQL: SELECT * FROM products ORDER BY price DESC LIMIT 5

Now generate a SQL query for this question:
Natural Language: {question}
SQL:"""


SQL_CODER_PROMPT = """-- Database Schema:
{schema_context}

-- Question: {question}
-- SQL Query:"""


ANTHROPIC_PROMPT = """You are a SQL expert. Given the following database schema and a natural language question, generate a valid SQL query.

Database Schema:
{schema_context}

Question: {question}

Generate ONLY the SQL query without any explanations or formatting. Do not include ```sql or any markdown."""


OPENAI_SYSTEM_PROMPT = """You are an expert SQL query generator. Convert natural language questions into valid SQL queries based on the provided database schema. Return only the SQL query without any explanations, markdown formatting, or additional text."""


OPENAI_USER_PROMPT = """Database Schema:
{schema_context}

Question: {question}

Generate the SQL query:"""


def get_prompt_template(provider: str, model: str = None) -> str:
    """
    Get the appropriate prompt template based on the provider and model
    
    Args:
        provider: LLM provider (huggingface, openai, anthropic)
        model: Specific model name (optional)
        
    Returns:
        Formatted prompt template
    """
    if provider == "huggingface":
        # Use specialized prompt for SQLCoder models
        if model and "sqlcoder" in model.lower():
            return SQL_CODER_PROMPT
        return SQL_GENERATION_PROMPT
    elif provider == "openai":
        return OPENAI_USER_PROMPT
    elif provider == "anthropic":
        return ANTHROPIC_PROMPT
    else:
        return SQL_GENERATION_PROMPT


def format_prompt(template: str, schema_context: str, question: str) -> str:
    """
    Format a prompt template with schema context and question
    
    Args:
        template: Prompt template string
        schema_context: Database schema information
        question: Natural language question
        
    Returns:
        Formatted prompt
    """
    return template.format(schema_context=schema_context, question=question)
