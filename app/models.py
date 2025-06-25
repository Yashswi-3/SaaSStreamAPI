from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    publication_date = Column(DateTime)
    category = Column(String)
    content = Column(Text)
    sentiment = Column(Float, nullable=True)

class ArticleStatistics(Base):
    __tablename__ = "article_statistics"
    id = Column(Integer, primary_key=True)
    category = Column(String, unique=True, nullable=False)
    count = Column(Integer, nullable=False)
