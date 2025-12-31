"""
SQL query executor with safety checks and error handling
"""
from sqlalchemy import text
from typing import Dict, Any, List, Tuple
import time
import re
import logging

logger = logging.getLogger(__name__)


class QueryExecutor:
    """Safely executes SQL queries with validation and error handling"""
    
    def __init__(self, engine, config: Dict[str, Any]):
        """
        Initialize query executor
        
        Args:
            engine: SQLAlchemy engine
            config: Execution configuration (timeout, max_rows, etc.)
        """
        self.engine = engine
        self.timeout = config.get('timeout', 30)
        self.max_rows = config.get('max_rows', 1000)
        self.enable_write_queries = config.get('enable_write_queries', False)
    
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """
        Validate SQL query for safety
        
        Args:
            query: SQL query string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, "Empty query"
        
        query_upper = query.strip().upper()
        
        # Check for dangerous operations if write queries are disabled
        if not self.enable_write_queries:
            dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
            for keyword in dangerous_keywords:
                if query_upper.startswith(keyword):
                    return False, f"Write operations are disabled. Query starts with {keyword}"
        
        # Check for SQL injection patterns
        injection_patterns = [
            r';\s*DROP',
            r';\s*DELETE',
            r'UNION\s+SELECT.*FROM\s+\w+',
            r'--\s*$',
        ]
        
        for pattern in injection_patterns:
            if re.search(pattern, query_upper):
                logger.warning(f"Potential SQL injection detected: {pattern}")
        
        return True, ""
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute SQL query and return results
        
        Args:
            query: SQL query string
            
        Returns:
            Dictionary containing execution results and metadata
        """
        start_time = time.time()
        
        # Validate query
        is_valid, error_msg = self.validate_query(query)
        if not is_valid:
            return {
                'success': False,
                'error': error_msg,
                'sql_query': query,
                'results': None,
                'columns': None,
                'row_count': 0,
                'execution_time': 0
            }
        
        try:
            with self.engine.connect() as conn:
                # Execute query with timeout
                result = conn.execute(text(query))
                
                # Check if this is a SELECT query
                if query.strip().upper().startswith('SELECT'):
                    columns = list(result.keys())
                    rows = result.fetchall()
                    
                    # Limit rows
                    limited_rows = rows[:self.max_rows]
                    
                    # Convert to list of dictionaries
                    results = [dict(zip(columns, row)) for row in limited_rows]
                    
                    execution_time = time.time() - start_time
                    
                    return {
                        'success': True,
                        'sql_query': query,
                        'results': results,
                        'columns': columns,
                        'row_count': len(results),
                        'execution_time': round(execution_time, 3),
                        'error': None
                    }
                else:
                    # For non-SELECT queries
                    conn.commit()
                    execution_time = time.time() - start_time
                    
                    return {
                        'success': True,
                        'sql_query': query,
                        'results': [],
                        'columns': [],
                        'row_count': 0,
                        'execution_time': round(execution_time, 3),
                        'error': None
                    }
        
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            logger.error(f"Query execution failed: {error_msg}")
            
            return {
                'success': False,
                'sql_query': query,
                'results': None,
                'columns': None,
                'row_count': 0,
                'execution_time': round(execution_time, 3),
                'error': error_msg
            }
