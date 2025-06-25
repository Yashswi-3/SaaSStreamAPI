import aiohttp
import asyncio
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class SentimentAPI:
    def __init__(self):
        # Using TextBlob as a free alternative, or you can use other APIs
        self.api_url = "https://api.meaningcloud.com/sentiment-2.1"
        self.api_key = "your_api_key_here"  # Replace with actual API key
        
    async def analyze_sentiment(self, text: str) -> Optional[float]:
        """Analyze sentiment using external API"""
        if not text or len(text.strip()) < 10:
            return 0.0
            
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    'key': self.api_key,
                    'txt': text[:1000],  # Limit text length
                    'lang': 'en'
                }
                
                async with session.post(self.api_url, data=payload, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Convert sentiment to numerical score
                        sentiment_map = {
                            'P+': 1.0,  # Strong positive
                            'P': 0.5,   # Positive
                            'NEU': 0.0, # Neutral
                            'N': -0.5,  # Negative
                            'N+': -1.0  # Strong negative
                        }
                        return sentiment_map.get(data.get('score_tag', 'NEU'), 0.0)
                    else:
                        logger.error(f"Sentiment API error: {response.status}")
                        return 0.0
                        
        except Exception as e:
            logger.error(f"Sentiment analysis error: {str(e)}")
            return 0.0

class NewsEnrichmentAPI:
    def __init__(self):
        self.sentiment_api = SentimentAPI()
        
    async def enrich_articles(self, articles: list) -> list:
        """Enrich articles with external API data"""
        enriched_articles = []
        
        # Process articles in batches to avoid rate limiting
        batch_size = 5
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            tasks = [self.enrich_single_article(article) for article in batch]
            enriched_batch = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in enriched_batch:
                if isinstance(result, dict):
                    enriched_articles.append(result)
                else:
                    logger.error(f"Enrichment error: {result}")
                    
            # Rate limiting delay
            await asyncio.sleep(1)
            
        return enriched_articles
        
    async def enrich_single_article(self, article: dict) -> dict:
        """Enrich a single article with sentiment and other data"""
        try:
            # Add sentiment analysis
            sentiment = await self.sentiment_api.analyze_sentiment(article.get('content', ''))
            article['sentiment'] = sentiment
            
            # Add word count
            article['word_count'] = len(article.get('content', '').split())
            
            # Add reading time estimate (average 200 words per minute)
            article['reading_time_minutes'] = max(1, article['word_count'] // 200)
            
            return article
            
        except Exception as e:
            logger.error(f"Error enriching article: {str(e)}")
            article['sentiment'] = 0.0
            article['word_count'] = 0
            article['reading_time_minutes'] = 1
            return article
