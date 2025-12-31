# Setup Guide

Complete installation and setup instructions for Agentic SQL.

## Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **npm**: 9 or higher
- **Git**: Latest version

### Optional Software

- **Docker**: 20.10 or higher (for containerized deployment)
- **Docker Compose**: 2.0 or higher

### Hardware Requirements

#### Minimum (Demo Mode)
- CPU: 2 cores
- RAM: 4 GB
- Disk: 2 GB free space

#### Recommended (With Local LLM)
- CPU: 4+ cores
- RAM: 16 GB (8 GB for 7B models with 8-bit quantization)
- GPU: NVIDIA GPU with 8+ GB VRAM (optional, for faster inference)
- Disk: 20 GB free space

## Installation Methods

### Method 1: Docker Deployment (Recommended)

#### Step 1: Clone Repository

```bash
git clone https://github.com/bishtNitin/agentic-sql.git
cd agentic-sql
```

#### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

#### Step 3: Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

#### Step 4: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

#### Step 5: Stop Services

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Method 2: Local Development Setup

#### Backend Setup

##### Step 1: Navigate to Backend

```bash
cd backend
```

##### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

##### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

##### Step 4: Setup Database

```bash
# Run database setup script
python setup_demo_db.py

# You should see:
# ✓ Demo database setup completed successfully!
```

##### Step 5: Configure Environment

```bash
# Copy example env file
cp ../.env.example .env

# Edit configuration
nano .env
```

##### Step 6: Start Backend

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m uvicorn app.main:app --reload
```

##### Step 7: Verify Backend

Open http://localhost:8000 - you should see:
```json
{
  "message": "Agentic SQL API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/health"
}
```

Visit http://localhost:8000/docs for API documentation.

#### Frontend Setup

##### Step 1: Navigate to Frontend (New Terminal)

```bash
cd frontend
```

##### Step 2: Install Dependencies

```bash
# Install npm packages
npm install

# Or using yarn
yarn install
```

##### Step 3: Configure Environment

```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

##### Step 4: Start Development Server

```bash
# Start Next.js dev server
npm run dev

# Or using yarn
yarn dev
```

##### Step 5: Access Application

Open http://localhost:3000 in your browser.

## Database Setup

### SQLite (Default - Demo)

SQLite is used by default for demo purposes. The database is created automatically when you run `setup_demo_db.py`.

**Location**: `backend/demo.db`

**Tables Created**:
- `employees` (50 rows)
- `departments` (5 rows)
- `products` (15 rows)
- `customers` (30 rows)
- `orders` (100 rows)

### PostgreSQL (Production)

#### Step 1: Install PostgreSQL

```bash
# macOS (using Homebrew)
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql

# Windows
# Download installer from postgresql.org
```

#### Step 2: Create Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE agentic_sql;
CREATE USER agentic_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE agentic_sql TO agentic_user;
\q
```

#### Step 3: Update Configuration

Edit `backend/.env`:
```bash
DATABASE_URL=postgresql://agentic_user:your_password@localhost:5432/agentic_sql
```

#### Step 4: Migrate Data

```python
# Create a migration script or manually recreate tables
# The schema can be found in setup_demo_db.py
```

## Environment Variables

### Backend Environment Variables

Create `backend/.env` with the following:

```bash
# Database Configuration
DATABASE_URL=sqlite:///./demo.db
# For PostgreSQL: postgresql://user:password@localhost:5432/dbname

# LLM Provider (huggingface, openai, anthropic)
LLM_PROVIDER=huggingface

# Hugging Face Settings
HUGGINGFACE_MODEL=defog/sqlcoder-7b-2

# OpenAI Settings (if using OpenAI)
# OPENAI_API_KEY=sk-...
# OPENAI_MODEL=gpt-4

# Anthropic Settings (if using Anthropic)
# ANTHROPIC_API_KEY=sk-ant-...
# ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Backend Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Environment Variables

Create `frontend/.env.local` with:

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running in Production

### Production Backend

#### Step 1: Install Production Dependencies

```bash
pip install gunicorn
```

#### Step 2: Run with Gunicorn

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### Production Frontend

#### Step 1: Build Application

```bash
cd frontend
npm run build
```

#### Step 2: Start Production Server

```bash
npm start
```

#### Step 3: Use Reverse Proxy (Recommended)

Configure nginx or similar:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Backend Issues

#### Issue: ModuleNotFoundError

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue: Database Connection Failed

**Solution**: Check DATABASE_URL in .env file and ensure database exists:
```bash
python setup_demo_db.py
```

#### Issue: Port 8000 Already in Use

**Solution**: Kill existing process or use different port:
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

#### Issue: LLM Model Loading Failed

**Solution**: For demo mode, the application uses fallback SQL generation. For production:
- Ensure sufficient memory (8+ GB)
- Check model name in config
- Use smaller models or 8-bit quantization

### Frontend Issues

#### Issue: API Connection Failed

**Solution**: Check NEXT_PUBLIC_API_URL in .env.local:
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
```

#### Issue: npm install Fails

**Solution**: Clear cache and reinstall:
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Issue: Build Errors

**Solution**: Check Node.js version:
```bash
node --version  # Should be 18+
npm --version   # Should be 9+
```

### Docker Issues

#### Issue: Container Fails to Start

**Solution**: Check logs:
```bash
docker-compose logs backend
docker-compose logs frontend
```

#### Issue: Port Conflicts

**Solution**: Change ports in docker-compose.yml:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Change host port
```

## Verification Steps

### 1. Backend Health Check

```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "database_connected": true,
  "llm_provider": "huggingface"
}
```

### 2. Frontend Accessibility

Open http://localhost:3000 - you should see the Agentic SQL interface.

### 3. End-to-End Test

1. Enter query: "Show all employees"
2. Click "Execute Query"
3. Verify SQL appears in right panel
4. Verify results table displays employee data

### 4. Schema Viewer Test

Check that the Schema Viewer sidebar shows:
- employees table
- departments table
- products table
- customers table
- orders table

## Next Steps

After successful setup:

1. Read [CONFIGURATION.md](CONFIGURATION.md) to customize LLM providers
2. Read [API.md](API.md) to understand API endpoints
3. Read [DEVELOPMENT.md](DEVELOPMENT.md) to start contributing
4. Try example queries and explore the database

## Support

If you encounter issues not covered here:

1. Check existing GitHub issues
2. Review logs for error messages
3. Create a new issue with:
   - Operating system
   - Python/Node version
   - Error messages
   - Steps to reproduce
