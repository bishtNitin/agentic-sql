"""
Database connection management using SQLAlchemy
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()


class DatabaseConnection:
    """Manages database connections and sessions"""
    
    def __init__(self, database_url: str):
        """
        Initialize database connection
        
        Args:
            database_url: SQLAlchemy database URL
        """
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the database engine and session factory"""
        try:
            # Create engine
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False} if "sqlite" in self.database_url else {},
                pool_pre_ping=True,
            )
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            logger.info(f"Database connection initialized: {self.database_url}")
        except Exception as e:
            logger.error(f"Failed to initialize database connection: {e}")
            raise
    
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session
        
        Yields:
            SQLAlchemy session
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def test_connection(self) -> bool:
        """
        Test if database connection is working
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def execute_raw_query(self, query: str, params: dict = None) -> list:
        """
        Execute a raw SQL query and return results
        
        Args:
            query: SQL query string
            params: Query parameters (optional)
            
        Returns:
            List of result rows as dictionaries
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                
                # For SELECT queries, fetch results
                if query.strip().upper().startswith("SELECT"):
                    columns = result.keys()
                    rows = result.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    # For other queries, commit and return empty list
                    conn.commit()
                    return []
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise
    
    def get_table_names(self) -> list:
        """
        Get list of all table names in the database
        
        Returns:
            List of table names
        """
        try:
            from sqlalchemy import inspect
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"Failed to get table names: {e}")
            raise
    
    def close(self):
        """Close the database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


# Global database connection instance
db_connection = None


def get_db_connection(database_url: str = None) -> DatabaseConnection:
    """
    Get or create the global database connection
    
    Args:
        database_url: Database URL (optional, uses existing if not provided)
        
    Returns:
        DatabaseConnection instance
    """
    global db_connection
    
    if db_connection is None and database_url:
        db_connection = DatabaseConnection(database_url)
    
    return db_connection
