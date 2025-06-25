from sqlalchemy.future import select
from sqlalchemy import func
from app.models import Article, ArticleStatistics
from app.schemas import ArticleCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def get_articles(db: AsyncSession, skip=0, limit=10, category=None, date=None):
    query = select(Article)
    if category:
        query = query.where(Article.category == category)
    if date:
        query = query.where(func.date(Article.publication_date) == date)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_article(db: AsyncSession, article_id: int):
    result = await db.execute(select(Article).where(Article.id == article_id))
    return result.scalar_one_or_none()

async def create_article(db: AsyncSession, article: ArticleCreate):
    db_article = Article(**article.dict())
    db.add(db_article)
    await db.commit()
    await db.refresh(db_article)
    return db_article

async def get_statistics(db: AsyncSession):
    result = await db.execute(select(Article.category, func.count()).group_by(Article.category))
    return [{"category": row[0], "count": row[1]} for row in result.all()]
