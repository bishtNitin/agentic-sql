"""
FastAPI Main Application
Entry point for the Agentic SQL backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys

from .config import config
from .database.connection import get_db_connection
from .agent.sql_agent import SQLAgent
from .api import routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Agentic SQL API",
    description="Natural Language to SQL Agent API - Convert English queries to SQL and execute them",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Agentic SQL API...")
    
    try:
        # Initialize database connection
        database_url = config.get_database_url()
        logger.info(f"Connecting to database: {database_url}")
        db_conn = get_db_connection(database_url)
        
        # Test connection
        if not db_conn.test_connection():
            logger.error("Failed to connect to database")
            raise RuntimeError("Database connection failed")
        
        logger.info("Database connection established")
        
        # Initialize SQL Agent
        llm_config = config.get_provider_config()
        execution_config = config.get_execution_config()
        
        logger.info(f"Initializing SQL Agent with provider: {llm_config.get('provider')}")
        
        routes.sql_agent = SQLAgent(
            llm_config=llm_config,
            engine=db_conn.engine,
            execution_config=execution_config
        )
        
        logger.info("SQL Agent initialized successfully")
        logger.info("Agentic SQL API is ready!")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info("Shutting down Agentic SQL API...")
    
    try:
        db_conn = get_db_connection()
        if db_conn:
            db_conn.close()
            logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Include API routes
app.include_router(routes.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Agentic SQL API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = config.settings.backend_host
    port = config.settings.backend_port
    
    logger.info(f"Starting server at {host}:{port}")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
