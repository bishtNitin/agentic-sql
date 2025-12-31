"""
API routes for the SQL Agent
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging
from datetime import datetime

from ..models.schemas import (
    QueryRequest,
    QueryResponse,
    SchemaResponse,
    TableListResponse,
    HealthResponse,
    QueryHistoryResponse,
    QueryHistoryItem,
)
from ..agent.sql_agent import SQLAgent
from ..database.connection import get_db_connection

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["api"])

# Global SQL agent instance
sql_agent = None

# Query history storage (in-memory for demo)
query_history = []


def get_sql_agent() -> SQLAgent:
    """Dependency to get SQL agent instance"""
    if sql_agent is None:
        raise HTTPException(status_code=500, detail="SQL Agent not initialized")
    return sql_agent


@router.post("/query", response_model=QueryResponse)
async def execute_query(
    request: QueryRequest,
    agent: SQLAgent = Depends(get_sql_agent)
):
    """
    Execute a natural language query
    
    - **query**: Natural language question to convert to SQL
    
    Returns the generated SQL, execution results, and metadata
    """
    try:
        logger.info(f"Received query: {request.query}")
        
        # Process the query
        result = agent.process_query(request.query)
        
        # Store in history
        history_item = {
            'id': len(query_history) + 1,
            'natural_query': request.query,
            'sql_query': result.get('sql_query', ''),
            'success': result.get('success', False),
            'timestamp': datetime.now()
        }
        query_history.append(history_item)
        
        # Keep only last 100 queries
        if len(query_history) > 100:
            query_history.pop(0)
        
        return QueryResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schema", response_model=SchemaResponse)
async def get_schema(agent: SQLAgent = Depends(get_sql_agent)):
    """
    Get the database schema information
    
    Returns information about all tables and their columns
    """
    try:
        schema_info = agent.get_schema_info()
        return SchemaResponse(**schema_info)
    except Exception as e:
        logger.error(f"Error getting schema: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables", response_model=TableListResponse)
async def get_tables(agent: SQLAgent = Depends(get_sql_agent)):
    """
    Get list of all database tables
    
    Returns a list of table names
    """
    try:
        tables = agent.get_table_list()
        return TableListResponse(tables=tables)
    except Exception as e:
        logger.error(f"Error getting tables: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=QueryHistoryResponse)
async def get_history(limit: int = 50):
    """
    Get query history
    
    - **limit**: Maximum number of history items to return (default: 50)
    
    Returns recent query history
    """
    try:
        # Get last N items
        recent_history = query_history[-limit:] if len(query_history) > limit else query_history
        
        # Reverse to show most recent first
        recent_history = list(reversed(recent_history))
        
        history_items = [QueryHistoryItem(**item) for item in recent_history]
        
        return QueryHistoryResponse(
            history=history_items,
            total=len(query_history)
        )
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns the health status of the API and its dependencies
    """
    try:
        db_conn = get_db_connection()
        db_connected = db_conn.test_connection() if db_conn else False
        
        from ..config import config
        llm_provider = config.get_provider_config().get('provider', 'unknown')
        
        return HealthResponse(
            status="healthy" if db_connected else "degraded",
            timestamp=datetime.now(),
            database_connected=db_connected,
            llm_provider=llm_provider
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(),
            database_connected=False,
            llm_provider="unknown"
        )
