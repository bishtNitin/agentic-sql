"""
Pydantic models for request/response schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for natural language query"""
    query: str = Field(..., description="Natural language query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Show me all employees with salary greater than 50000"
            }
        }


class QueryResponse(BaseModel):
    """Response model for query execution"""
    success: bool = Field(..., description="Whether the query was successful")
    sql_query: Optional[str] = Field(None, description="Generated SQL query")
    results: Optional[List[Dict[str, Any]]] = Field(None, description="Query results")
    columns: Optional[List[str]] = Field(None, description="Column names")
    row_count: Optional[int] = Field(None, description="Number of rows returned")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    error: Optional[str] = Field(None, description="Error message if any")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "sql_query": "SELECT * FROM employees WHERE salary > 50000",
                "results": [{"id": 1, "name": "John Doe", "salary": 60000}],
                "columns": ["id", "name", "salary"],
                "row_count": 1,
                "execution_time": 0.15,
                "error": None
            }
        }


class TableSchema(BaseModel):
    """Schema information for a database table"""
    table_name: str
    columns: List[Dict[str, str]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "table_name": "employees",
                "columns": [
                    {"name": "id", "type": "INTEGER"},
                    {"name": "name", "type": "VARCHAR"},
                    {"name": "salary", "type": "INTEGER"}
                ]
            }
        }


class SchemaResponse(BaseModel):
    """Response model for database schema"""
    tables: List[TableSchema]
    
    class Config:
        json_schema_extra = {
            "example": {
                "tables": [
                    {
                        "table_name": "employees",
                        "columns": [
                            {"name": "id", "type": "INTEGER"},
                            {"name": "name", "type": "VARCHAR"}
                        ]
                    }
                ]
            }
        }


class TableListResponse(BaseModel):
    """Response model for table list"""
    tables: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "tables": ["employees", "departments", "products"]
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    timestamp: datetime
    database_connected: bool
    llm_provider: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T00:00:00",
                "database_connected": True,
                "llm_provider": "huggingface"
            }
        }


class QueryHistoryItem(BaseModel):
    """Model for query history item"""
    id: int
    natural_query: str
    sql_query: str
    success: bool
    timestamp: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "natural_query": "Show all employees",
                "sql_query": "SELECT * FROM employees",
                "success": True,
                "timestamp": "2024-01-01T00:00:00"
            }
        }


class QueryHistoryResponse(BaseModel):
    """Response model for query history"""
    history: List[QueryHistoryItem]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "history": [],
                "total": 0
            }
        }
