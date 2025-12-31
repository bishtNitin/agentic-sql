# Agentic SQL - Natural Language to SQL Agent

<div align="center">

![Agentic SQL](https://img.shields.io/badge/Agentic-SQL-blue)
![Python](https://img.shields.io/badge/Python-3.11+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-blue)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

**Transform English queries into SQL and execute them with an intelligent AI agent**

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Demo](#demo)

</div>

---

## 🎯 Overview

Agentic SQL is a production-ready application that empowers non-technical users to query databases using natural language. Simply type your question in plain English, and watch as the AI agent converts it into SQL, executes it, and presents the results in a beautiful, modern interface.

### Unique Selling Proposition (USP)

**Democratize Data Access**: Enable anyone in your organization—from executives to support staff—to access and analyze data without SQL knowledge. No more waiting on data analysts or learning complex query languages.

### Key Features

✨ **Natural Language Understanding**: Ask questions in plain English
🔄 **Multi-Model Support**: Switch between open-source (Hugging Face) and paid (OpenAI, Anthropic) models
🎨 **Modern Web UI**: Beautiful split-screen interface with dark/light mode
🔍 **Schema Browser**: Explore your database structure visually
📊 **Real-time Results**: See SQL generation and execution in real-time
📜 **Query History**: Track and reuse past queries
🔒 **Safe Execution**: Built-in SQL injection prevention
🚀 **Production Ready**: Docker support, comprehensive error handling
🌐 **Extensible**: Designed for easy addition of new languages (Hindi, etc.)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)

### Option 1: Run with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/bishtNitin/agentic-sql.git
cd agentic-sql

# Copy environment file
cp .env.example .env

# Start the application
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Run Locally

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup demo database
python setup_demo_db.py

# Start the backend
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
# Navigate to frontend (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

Access the application at `http://localhost:3000`

---

## 📸 Demo

### Interface Overview

The application features a clean, intuitive split-screen design:

- **Left Panel**: Natural language input with example queries
- **Right Panel**: Generated SQL and results display
- **Left Sidebar**: Database schema browser and query history

### Example Queries

Try these sample queries:

- "Show all employees"
- "Find employees with salary greater than 60000"
- "Count employees by department"
- "Show top 5 products by price"
- "List all customers from New York"
- "What is the average salary by department?"

---

## 🛠 Technology Stack

### Backend
- **FastAPI**: High-performance async API framework
- **SQLAlchemy**: SQL ORM for database abstraction
- **LangChain**: Agent orchestration framework
- **Hugging Face Transformers**: Open-source LLM support
- **OpenAI/Anthropic**: Optional paid model integrations

### Frontend
- **Next.js 16**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality UI components
- **React Syntax Highlighter**: SQL code highlighting

### Database
- **SQLite**: Demo database (included)
- **PostgreSQL**: Production support

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture and design decisions
- **[SETUP.md](docs/SETUP.md)**: Detailed installation and configuration guide
- **[CONFIGURATION.md](docs/CONFIGURATION.md)**: Model configuration and switching
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)**: Contributing and extending the application
- **[API.md](docs/API.md)**: API endpoints and usage

---

## ⚙️ Configuration

### Switching Between Models

Edit `backend/config.yaml` to switch between different LLM providers:

```yaml
# Use Hugging Face (default, free)
provider: huggingface
huggingface:
  default_model: defog/sqlcoder-7b-2

# Or use OpenAI
provider: openai
# Set OPENAI_API_KEY in .env

# Or use Anthropic
provider: anthropic
# Set ANTHROPIC_API_KEY in .env
```

See [CONFIGURATION.md](docs/CONFIGURATION.md) for detailed configuration options.

---

## 🤝 Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](docs/DEVELOPMENT.md) for guidelines on:

- Adding new LLM models
- Extending language support
- Code style and best practices
- Testing procedures

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **defog.ai** for SQLCoder models
- **Hugging Face** for model hosting
- **FastAPI** and **Next.js** communities
- All open-source contributors

---

## 📧 Contact

For questions, issues, or suggestions:

- Open an issue on GitHub
- Email: [your-email@example.com]

---

<div align="center">

**Made with ❤️ for democratizing data access**

[⬆ Back to Top](#agentic-sql---natural-language-to-sql-agent)

</div>
