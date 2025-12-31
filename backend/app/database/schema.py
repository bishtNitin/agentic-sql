"""
Database schema introspection utilities
"""
from sqlalchemy import inspect, MetaData
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class SchemaIntrospector:
    """Inspects database schema to provide context for SQL generation"""
    
    def __init__(self, engine):
        """
        Initialize schema introspector
        
        Args:
            engine: SQLAlchemy engine
        """
        self.engine = engine
        self.inspector = inspect(engine)
        self.metadata = MetaData()
    
    def get_all_tables(self) -> List[str]:
        """
        Get list of all table names
        
        Returns:
            List of table names
        """
        try:
            return self.inspector.get_table_names()
        except Exception as e:
            logger.error(f"Failed to get table names: {e}")
            return []
    
    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get detailed schema for a specific table
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with table schema information
        """
        try:
            columns = self.inspector.get_columns(table_name)
            primary_keys = self.inspector.get_pk_constraint(table_name)
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            indexes = self.inspector.get_indexes(table_name)
            
            return {
                'table_name': table_name,
                'columns': columns,
                'primary_keys': primary_keys.get('constrained_columns', []),
                'foreign_keys': foreign_keys,
                'indexes': indexes
            }
        except Exception as e:
            logger.error(f"Failed to get schema for table {table_name}: {e}")
            return {}
    
    def get_all_schemas(self) -> List[Dict[str, Any]]:
        """
        Get schemas for all tables in the database
        
        Returns:
            List of table schemas
        """
        tables = self.get_all_tables()
        return [self.get_table_schema(table) for table in tables]
    
    def get_schema_context(self) -> str:
        """
        Generate a context string describing the database schema
        This is used to provide context to the LLM for SQL generation
        
        Returns:
            Formatted schema context string
        """
        tables = self.get_all_tables()
        
        if not tables:
            return "No tables found in database."
        
        context_parts = ["Database Schema:\n"]
        
        for table_name in tables:
            schema = self.get_table_schema(table_name)
            context_parts.append(f"\nTable: {table_name}")
            
            # Add columns
            columns_info = []
            for col in schema.get('columns', []):
                col_name = col['name']
                col_type = str(col['type'])
                nullable = "NULL" if col.get('nullable', True) else "NOT NULL"
                
                col_desc = f"  - {col_name} ({col_type}, {nullable})"
                
                # Mark primary keys
                if col_name in schema.get('primary_keys', []):
                    col_desc += " PRIMARY KEY"
                
                columns_info.append(col_desc)
            
            context_parts.extend(columns_info)
            
            # Add foreign key relationships
            foreign_keys = schema.get('foreign_keys', [])
            if foreign_keys:
                context_parts.append("  Foreign Keys:")
                for fk in foreign_keys:
                    fk_cols = ', '.join(fk.get('constrained_columns', []))
                    ref_table = fk.get('referred_table', '')
                    ref_cols = ', '.join(fk.get('referred_columns', []))
                    context_parts.append(f"    - {fk_cols} -> {ref_table}({ref_cols})")
        
        return '\n'.join(context_parts)
    
    def get_table_sample_data(self, table_name: str, limit: int = 3) -> List[Dict]:
        """
        Get sample rows from a table
        
        Args:
            table_name: Name of the table
            limit: Number of sample rows to retrieve
            
        Returns:
            List of sample rows as dictionaries
        """
        try:
            from sqlalchemy import text
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                columns = result.keys()
                rows = result.fetchall()
                return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"Failed to get sample data for {table_name}: {e}")
            return []
