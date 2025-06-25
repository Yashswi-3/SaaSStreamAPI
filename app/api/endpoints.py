from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import ArticleRead, ArticleCreate, ArticleStatisticsRead
from app.crud import get_articles, get_article, create_article, get_statistics
from app.scraper import TheSaaSNewsScraper
from app.api.external_api import NewsEnrichmentAPI
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/articles/", response_model=list[ArticleRead])
async def read_articles(
    skip: int = 0,
    limit: int = 10,
    category: str = None,
    date: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get articles with optional filtering"""
    try:
        return await get_articles(db, skip=skip, limit=limit, category=category, date=date)
    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching articles")

@router.get("/article/{article_id}", response_model=ArticleRead)
async def read_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific article by ID"""
    try:
        article = await get_article(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article {article_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching article")

@router.post("/articles/", response_model=ArticleRead)
async def add_article(article: ArticleCreate, db: AsyncSession = Depends(get_db)):
    """Add a new article"""
    try:
        return await create_article(db, article)
    except Exception as e:
        logger.error(f"Error creating article: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating article")

@router.get("/article-statistics/", response_model=list[ArticleStatisticsRead])
async def article_statistics(db: AsyncSession = Depends(get_db)):
    """Get article statistics by category"""
    try:
        return await get_statistics(db)
    except Exception as e:
        logger.error(f"Error fetching statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching statistics")

@router.post("/scrape/", response_model=dict)
async def scrape_and_store(
    background_tasks: BackgroundTasks,
    max_pages: int = 3,
    db: AsyncSession = Depends(get_db)
):
    """Scrape TheSaaSNews and store articles with enrichment"""
    try:
        scraper = TheSaaSNewsScraper()
        enrichment_api = NewsEnrichmentAPI()
        
        # Scrape articles
        logger.info(f"Starting scrape of {max_pages} pages")
        articles = await scraper.scrape_all_pages(max_pages)
        
        if not articles:
            return {"message": "No articles found", "count": 0}
        
        # Enrich articles with external API data
        logger.info(f"Enriching {len(articles)} articles")
        enriched_articles = await enrichment_api.enrich_articles(articles)
        
        # Store in database
        stored_count = 0
        for article_data in enriched_articles:
            try:
                await create_article(db, ArticleCreate(**article_data))
                stored_count += 1
            except Exception as e:
                logger.error(f"Error storing article: {str(e)}")
                continue
        
        return {
            "message": f"Successfully scraped and stored {stored_count} articles",
            "scraped_count": len(articles),
            "stored_count": stored_count,
            "enriched_count": len(enriched_articles)
        }
        
    except Exception as e:
        logger.error(f"Scraping error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")
