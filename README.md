# 🚀 SaaS News API Pipeline

<div align="center">

*A comprehensive Python backend application that leverages FastAPI to create a high-performance API for SaaS news articles, combining web scraping capabilities with data processing, optional API integration, and database management.*

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

The **SaaS News API Pipeline** is a backend application built with FastAPI that scrapes SaaS news articles from online sources, processes the data, and serves it through a structured and scalable REST API. The application is organized using object-oriented principles and modular design for maintainability and future extensibility.

**🔗 GitHub Repository**: [https://github.com/Yashswi-3/SaaSStreamAPI](https://github.com/Yashswi-3/SaaSStreamAPI)

### Key Highlights

- **🔄 Asynchronous Operations**: Built with `async/await` for high concurrency  
- **🕷️ Web Scraping**: Generic scraping logic with support for customization  
- **💾 Robust Database**: SQLAlchemy ORM with SQLite integration  
- **📊 Data Processing**: Data cleaning, transformation, and categorization pipeline  
- **🎨 Clean Architecture**: Modular codebase following OOP principles  

## ✨ Features

### Core Functionality
- ✅ **Web Scraping**: Configurable scraper using BeautifulSoup (currently uses generic selectors)  
- ✅ **Data Processing**: Text cleanup, date parsing, URL normalization  
- ✅ **Database Management**: SQLite integration via SQLAlchemy ORM  
- ✅ **REST API**: Create, read, and filter articles with pagination  
- ✅ **Modular Design**: Clear separation of scraping, processing, and API layers  

### Optional/Planned Features
- 🧠 **Optional Sentiment Analysis**: Placeholder structure for future external API enrichment  
- 🧪 **Testing Improvements**: Basic test structure in place, more tests under development  

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Web Framework** | FastAPI | Async API development |
| **Database ORM** | SQLAlchemy | Data modeling and persistence |
| **Scraping** | BeautifulSoup4 | Web data extraction |
| **HTTP Clients** | httpx / aiohttp | API calls (optional) |
| **Validation** | Pydantic | Schema validation |
| **Database** | SQLite (default) | Lightweight storage |
| **Testing** | pytest (basic) | Test structure setup |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip or conda

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

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Access the API**
- 📖 **Docs**: http://127.0.0.1:8000/docs  
- 🔗 **Base URL**: http://127.0.0.1:8000  
- 📋 **ReDoc**: http://127.0.0.1:8000/redoc  

## 📁 Project Structure

```
saas_news_api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy models
│   ├── database.py          # DB session and init
│   ├── schemas.py           # Pydantic schemas
│   ├── scraper.py           # Generic web scraper
│   ├── crud.py              # DB operations
│   ├── utils.py             # Data processing tools
│   └── api/
│       ├── endpoints.py     # FastAPI routes
│       └── external_api.py  # Placeholder for API integration
├── tests/
│   └── test_endpoints.py    # Basic tests (WIP)
├── requirements.txt
└── README.md
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/articles/` | List articles (supports filters: category, date) |
| `GET` | `/article/{id}` | Fetch article by ID |
| `POST` | `/articles/` | Create a new article |
| `GET` | `/article-statistics/` | View article counts per category |
| `POST` | `/scrape/` | Trigger scraping process |

### Example Usage

```bash
# Filter by category
curl -X GET "http://127.0.0.1:8000/articles/?category=Tech"

# Trigger scraping
curl -X POST "http://127.0.0.1:8000/scrape/?max_pages=3"
```

## ⚙️ Configuration

### Environment Variables

```env
# SQLite default
DATABASE_URL=sqlite+aiosqlite:///./news.db

# PostgreSQL (unverified)
# DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname

# Optional external API
SENTIMENT_API_KEY=your_sentiment_api_key
SENTIMENT_API_URL=https://api.example.com/analyze
```

### Note:
- The code is currently tested with SQLite.
- PostgreSQL setup is present but may require extra configuration and verification.

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Current Coverage
- ✅ Basic endpoint testing  
- 🟡 Scraper and DB testing in progress  
- 🟡 External API test structure present (placeholder)  

## 🏗️ Architecture

```
┌───────────────┐     ┌───────────────┐
│ Web Scraper   │     │ FastAPI Routes│
│(BeautifulSoup)│     │  (endpoints)  │
└──────┬────────┘     └──────┬────────┘
       ▼                         ▼
        ┌───────────────────────────────────────────────┐
        │ Data Processing (cleaning, formatting, logic) │
        └────────────────────┬──────────────────────────┘
                             ▼
             ┌────────────────────────────────────┐
             │ SQLite DB via SQLAlchemy ORM       │
             └────────────────────────────────────┘
```

### Design Practices
- OOP modular design  
- Dependency Injection using FastAPI  
- Clean separation of logic per layer  

## 📊 Performance Features

- ✅ Async/await throughout the application  
- ✅ Database connection pooling  
- ✅ Optimized for concurrent operations  
- ✅ Pagination for large datasets  

> ⚠️ Note: No formal benchmarking has been done yet. Claims are based on design intentions, not tested metrics.

## 🤝 Contributing

We welcome contributions!  

1. Fork the repo  
2. Create your feature branch: `git checkout -b feature/my-feature`  
3. Commit your changes  
4. Push and open a Pull Request  

### Dev Guidelines
- Follow PEP 8  
- Keep code modular  
- Write or update tests where relevant  
- Test all changes before PR  


## 🙏 Acknowledgments

- **FastAPI**  
- **SQLAlchemy**  
- **BeautifulSoup4**  
- **Pydantic**  

---

<div align="center">

**Built with ❤️ by [Yashswi Shukla](https://github.com/Yashswi-3)**  
🔗 [Portfolio](https://yashswi-3.github.io/Portfolio/)  
🔗 [GitHub](https://github.com/Yashswi-3)  
🔗 [LinkedIn](https://www.linkedin.com/in/yashswi-shukla-8384ba252)  

⭐ Star this repo if you find it helpful!

</div>
