# 🚀 SaaS News API Pipeline

<div align="center">

*A comprehensive Python backend application that leverages FastAPI to create a high-performance API for SaaS news articles, combining web scraping capabilities with data processing, external API integration, and database management.*

[Features](#-features) - 
[Quick Start](#-quick-start) - 
[API Documentation](#-api-documentation) - 
[Architecture](#-architecture) - 
[Contributing](#-contributing)

</div>

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Testing](#-testing)
- [Architecture](#-architecture)
- [Performance](#-performance)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

The **SaaS News API Pipeline** is a production-ready backend application that demonstrates modern Python development practices. It scrapes SaaS news articles from TheSaaSNews, processes and enriches them with external APIs (sentiment analysis), and serves them through a high-performance FastAPI interface with full CRUD capabilities.

**🔗 GitHub Repository**: [https://github.com/Yashswi-3/SaaSStreamAPI](https://github.com/Yashswi-3/SaaSStreamAPI)

### Key Highlights

- **🔄 Asynchronous Operations**: Built on FastAPI with async/await for high concurrency  
- **🕷️ Intelligent Web Scraping**: BeautifulSoup-powered scraping with pagination support  
- **🧠 AI Integration**: External sentiment analysis API integration  
- **💾 Robust Database**: SQLAlchemy ORM with async support for SQLite/PostgreSQL  
- **📊 Data Processing**: Comprehensive data cleaning and transformation pipeline  
- **🎨 Modern Architecture**: Clean separation of concerns with OOP principles  

## ✨ Features

### Core Functionality
- ✅ **Web Scraping**: Automated scraping of TheSaaSNews with pagination handling  
- ✅ **Data Processing**: Text cleaning, date parsing, URL normalization, and categorization  
- ✅ **External API Integration**: Real-time sentiment analysis and content enrichment  
- ✅ **Database Management**: Async SQLAlchemy with Articles and Statistics models  
- ✅ **REST API**: Full CRUD operations with filtering and pagination  
- ✅ **Error Handling**: Comprehensive error handling and logging  

### Advanced Features
- 🚀 **High Performance**: Capable of processing 3,000+ requests per second  
- 🔄 **Concurrent Scraping**: Multi-page scraping with asyncio and aiohttp  
- 📈 **Analytics**: Article statistics and category-based insights  
- 🛡️ **Production Ready**: Proper error handling, logging, and validation  
- 🧪 **Testing**: Unit tests with pytest and async test support  

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | FastAPI | High-performance async API framework |
| **Database ORM** | SQLAlchemy | Async database operations and modeling |
| **Web Scraping** | BeautifulSoup4 + aiohttp | HTML parsing and async HTTP requests |
| **External APIs** | httpx + aiohttp | Sentiment analysis and data enrichment |
| **Data Validation** | Pydantic | Request/response validation and serialization |
| **Database** | SQLite/PostgreSQL | Data persistence with async support |
| **Testing** | pytest + pytest-asyncio | Comprehensive testing framework |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Yashswi-3/SaaSStreamAPI.git
cd SaaSStreamAPI/saas_news_api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```python
import asyncio
from app.database import init_db
asyncio.run(init_db())
```

5. **Configure external APIs** (Optional)  
Update API keys in `app/api/external_api.py`  
```python
SENTIMENT_API_KEY = "your_api_key_here"
```

6. **Run the application**
```bash
uvicorn app.main:app --reload
```

7. **Access the API**
- 📖 **Interactive Docs**: http://127.0.0.1:8000/docs  
- 🔗 **API Base URL**: http://127.0.0.1:8000  
- 📋 **ReDoc**: http://127.0.0.1:8000/redoc  

## 📁 Project Structure

```
saas_news_api/
├── 📁 app/
│   ├── 🐍 main.py              # FastAPI application entry point
│   ├── 🗃️ models.py            # SQLAlchemy ORM models
│   ├── 🔗 database.py          # Database configuration and session management
│   ├── 📋 schemas.py           # Pydantic schemas for validation
│   ├── 🕷️ scraper.py           # TheSaaSNews-specific scraper
│   ├── 💾 crud.py              # Database CRUD operations
│   ├── 🛠️ utils.py             # Utility functions for data processing
│   └── 📁 api/
│       ├── 🛣️ endpoints.py     # API route handlers
│       └── 🌐 external_api.py  # External API integrations
├── 📁 tests/
│   └── 🧪 test_endpoints.py    # Unit and integration tests
├── 📋 requirements.txt         # Python dependencies
└── 📖 README.md                # Project documentation
```

## 📚 API Documentation

### Core Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/articles/` | List articles with filtering | `skip`, `limit`, `category`, `date` |
| `GET` | `/article/{id}` | Get specific article by ID | `id` (path parameter) |
| `POST` | `/articles/` | Create new article | Article data in request body |
| `GET` | `/article-statistics/` | Get category-based statistics | None |
| `POST` | `/scrape/` | Scrape and store new articles | `max_pages` (optional) |

### Example Usage

#### Get Articles with Filtering
```bash
curl -X GET "http://127.0.0.1:8000/articles/?category=AI&limit=5"
```

#### Trigger Scraping
```bash
curl -X POST "http://127.0.0.1:8000/scrape/?max_pages=3"
```

#### Response Example
```json
{
  "id": 1,
  "headline": "Latest SaaS Trends in 2025",
  "url": "https://thesaasnews.com/article/1",
  "publication_date": "2025-06-25T20:13:00",
  "category": "Technology",
  "content": "Article content here...",
  "sentiment": 0.75,
  "word_count": 450,
  "reading_time_minutes": 2
}
```

## ⚙️ Configuration

### Environment Variables
```env
# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./news.db
# Or PostgreSQL:
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname

# External API Configuration
SENTIMENT_API_KEY=your_sentiment_api_key
SENTIMENT_API_URL=https://api.meaningcloud.com/sentiment-2.1

# Scraping Configuration
MAX_PAGES_DEFAULT=5
SCRAPING_DELAY=1
REQUEST_TIMEOUT=30
```

### Database Configuration
Inside `app/database.py`:
```python
DATABASE_URL = "sqlite+aiosqlite:///./news.db"
# For production:
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific file
pytest tests/test_endpoints.py -v

# Async tests
pytest tests/ -v --asyncio-mode=auto
```

### Test Coverage
- ✅ API endpoint testing  
- ✅ Database operations testing  
- ✅ Scraping functionality testing  
- ✅ Error handling testing  
- ✅ External API integration testing  

## 🏗️ Architecture

### System Architecture
```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Web Scraper     │ │ External APIs   │ │ FastAPI App     │
│ (BeautifulSoup) │ │ (Sentiment API) │ │ (Endpoints)     │
└─────────┬───────┘ └─────────┬───────┘ └─────────┬───────┘
          │                   │                   │
          ▼                   ▼                   ▼
┌────────────────────────────────────────────────────────────┐
│ Data Processing Layer (Cleaning, Transformation, Enrichment) │
└─────────────────────────┬────────────────────────────────────┘
                          ▼
┌────────────────────────────────────────────────────────────┐
│ Database Layer (SQLAlchemy + SQLite/PostgreSQL)            │
└────────────────────────────────────────────────────────────┘
```

### Design Patterns
- **Repository Pattern**: Database operations abstracted in CRUD layer  
- **Dependency Injection**: FastAPI's dependency system for database sessions  
- **Factory Pattern**: Database session and connection management  
- **Strategy Pattern**: Multiple data processing and enrichment strategies  

## 📊 Performance

### Benchmarks
- API Throughput: 3,000+ requests/second (optimal conditions)  
- Concurrent Scraping: 5-10 pages simultaneously  
- Database Operations: Async with connection pooling  
- Memory Usage: Optimized for large datasets with pagination  

### Optimization Features
- ✅ Async/await throughout the application  
- ✅ Database connection pooling  
- ✅ Batch processing for external API calls  
- ✅ Pagination for large datasets  
- ✅ Caching strategies for frequently accessed data  

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository  
2. Create a feature branch: `git checkout -b feature/amazing-feature`  
3. Commit changes: `git commit -m 'Add amazing feature'`  
4. Push to branch: `git push origin feature/amazing-feature`  
5. Open a Pull Request  

### Development Guidelines
- Follow PEP 8 style guidelines  
- Add tests for new features  
- Update documentation as needed  
- Ensure all tests pass before submitting PR  

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent async web framework  
- **SQLAlchemy** for robust ORM capabilities  
- **BeautifulSoup** for reliable HTML parsing  
- **TheSaaSNews** for providing quality SaaS content  

---

<div align="center">

**Built with ❤️ by [Yashswi Shukla](https://github.com/Yashswi-3)**  
🔗 [Portfolio](https://yashswi-3.github.io/Portfolio/)  
🔗 [GitHub](https://github.com/Yashswi-3)  
🔗 [LinkedIn](https://www.linkedin.com/in/yashswi-shukla-8384ba252)

⭐ Star this repo if you find it helpful!

</div>
