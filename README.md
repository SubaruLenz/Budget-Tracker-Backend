# Budget Tracker Backend

A FastAPI-based backend service for personal budget tracking with AI-powered conversation features.

## Features

- 🔐 JWT Authentication
- 💰 Transaction Management
- 👛 Wallet Management
- 📊 Category Management
- 🤖 AI-Powered Budget Conversations
- 🐳 Docker Support
- 📝 Comprehensive Logging

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **AI Integration**: AWS Bedrock (Claude 3 Haiku)
- **Secrets Management**: AWS Secrets Manager
- **Containerization**: Docker

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Budget-Tracker-Backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp app/.env.example app/.env
# Edit app/.env with your configuration
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

### Docker Setup

```bash
docker build -t budget-tracker-backend .
docker run -p 8000:8000 budget-tracker-backend
```

## API Endpoints

- **Health Check**: `/health`
- **Authentication**: `/auth/*`
- **Wallets**: `/wallets/*`
- **Transactions**: `/transactions/*`
- **Categories**: `/categories/*`
- **Conversations**: `/conversations/*`

## Project Structure

```
app/
├── authentication/     # JWT authentication logic
├── config/            # Configuration and logging
├── database/          # Database models and schemas
├── llm/              # AI/LLM integration
├── router/           # API route handlers
└── main.py           # Application entry point
```

## Environment Variables

Create `app/.env` with:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
# AWS Secrets Manager and Bedrock configuration
```

## Development

### Running Tests

```bash
python -m pytest test/
```

### Database Reset

```bash
python test/reset_main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License