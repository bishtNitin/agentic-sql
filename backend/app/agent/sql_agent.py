"""
SQL Agent - Main orchestration logic for natural language to SQL conversion
"""
from typing import Dict, Any
import logging
from .llm_provider import create_llm_provider
from .prompts import get_prompt_template, format_prompt
from ..database.schema import SchemaIntrospector
from ..database.executor import QueryExecutor

logger = logging.getLogger(__name__)


class SQLAgent:
    """
    Main SQL Agent that coordinates the natural language to SQL pipeline
    """
    
    def __init__(self, llm_config: Dict[str, Any], engine, execution_config: Dict[str, Any]):
        """
        Initialize SQL Agent
        
        Args:
            llm_config: LLM provider configuration
            engine: SQLAlchemy database engine
            execution_config: Query execution configuration
        """
        self.llm_config = llm_config
        self.engine = engine
        self.execution_config = execution_config
        
        # Initialize components
        self.llm_provider = create_llm_provider(llm_config)
        self.schema_introspector = SchemaIntrospector(engine)
        self.query_executor = QueryExecutor(engine, execution_config)
        
        # Cache schema context
        self.schema_context = self.schema_introspector.get_schema_context()
        
        logger.info(f"SQL Agent initialized with provider: {llm_config.get('provider')}")
    
    def process_query(self, natural_language_query: str) -> Dict[str, Any]:
        """
        Process a natural language query end-to-end
        
        Args:
            natural_language_query: User's question in natural language
            
        Returns:
            Dictionary with SQL query, results, and metadata
        """
        try:
            # Step 1: Generate SQL from natural language
            logger.info(f"Processing query: {natural_language_query}")
            sql_query = self.generate_sql(natural_language_query)
            logger.info(f"Generated SQL: {sql_query}")
            
            # Step 2: Execute the generated SQL
            result = self.query_executor.execute(sql_query)
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'success': False,
                'sql_query': None,
                'results': None,
                'columns': None,
                'row_count': 0,
                'execution_time': 0,
                'error': str(e)
            }
    
    def generate_sql(self, natural_language_query: str) -> str:
        """
        Generate SQL query from natural language
        
        Args:
            natural_language_query: User's question in natural language
            
        Returns:
            Generated SQL query string
        """
        # Get appropriate prompt template
        provider = self.llm_config.get('provider')
        model = self.llm_config.get('model')
        template = get_prompt_template(provider, model)
        
        # Format prompt with schema context and question
        prompt = format_prompt(template, self.schema_context, natural_language_query)
        
        # Generate SQL using LLM
        sql_query = self.llm_provider.generate(prompt)
        
        # Clean up the generated SQL
        sql_query = self._clean_sql(sql_query)
        
        return sql_query
    
    def _clean_sql(self, sql: str) -> str:
        """
        Clean up generated SQL query
        
        Args:
            sql: Raw SQL query from LLM
            
        Returns:
            Cleaned SQL query
        """
        # Remove common artifacts
        sql = sql.strip()
        
        # Remove markdown code blocks
        sql = sql.replace("```sql", "").replace("```", "")
        
        # Remove leading/trailing whitespace
        sql = sql.strip()
        
        # Remove trailing semicolon if present (will be added back if needed)
        if sql.endswith(';'):
            sql = sql[:-1].strip()
        
        return sql
    
    def get_schema_info(self) -> Dict[str, Any]:
        """
        Get database schema information
        
        Returns:
            Dictionary with schema information
        """
        schemas = self.schema_introspector.get_all_schemas()
        
        formatted_tables = []
        for schema in schemas:
            table_info = {
                'table_name': schema['table_name'],
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type'])
                    }
                    for col in schema['columns']
                ]
            }
            formatted_tables.append(table_info)
        
        return {'tables': formatted_tables}
    
    def get_table_list(self) -> list:
        """
        Get list of all tables
        
        Returns:
            List of table names
        """
        return self.schema_introspector.get_all_tables()
    
    def refresh_schema(self):
        """Refresh the cached schema context"""
        self.schema_context = self.schema_introspector.get_schema_context()
        logger.info("Schema context refreshed")
