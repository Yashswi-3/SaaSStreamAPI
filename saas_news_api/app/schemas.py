from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

class ArticleBase(BaseModel):
    headline: str
    url: HttpUrl
    publication_date: datetime | None = None
    category: str | None = None
    content: str | None = None
    sentiment: float | None = None

class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: int
    class Config:
        from_attributes = True

class ArticleStatisticsRead(BaseModel):
    category: str
    count: int
    class Config:
        from_attributes = True
