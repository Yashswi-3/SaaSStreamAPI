import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class TheSaaSNewsScraper:
    def __init__(self):
        self.base_url = "https://thesaasnews.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetch a single page with error handling"""
        try:
            async with session.get(url, headers=self.headers, timeout=30) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    logger.error(f"HTTP {response.status} for {url}")
                    return ""
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            return ""
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    def extract_article_data(self, article_element, base_url: str) -> Dict:
        """Extract data from a single article element"""
        try:
            # TheSaaSNews-specific selectors (adjust based on actual site structure)
            headline_elem = article_element.find('h2', class_='entry-title') or article_element.find('h3', class_='entry-title')
            headline = headline_elem.get_text(strip=True) if headline_elem else "No title"
            
            # Extract URL
            link_elem = headline_elem.find('a') if headline_elem else article_element.find('a')
            url = urljoin(base_url, link_elem['href']) if link_elem and link_elem.get('href') else ""
            
            # Extract date
            date_elem = article_element.find('time') or article_element.find(class_='entry-date')
            date_str = date_elem.get('datetime') or date_elem.get_text(strip=True) if date_elem else ""
            publication_date = self.parse_date(date_str)
            
            # Extract category
            category_elem = article_element.find(class_='category') or article_element.find('span', class_='cat-links')
            category = category_elem.get_text(strip=True) if category_elem else "General"
            
            # Extract content/summary
            content_elem = article_element.find(class_='entry-summary') or article_element.find('p')
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            return {
                'headline': headline,
                'url': url,
                'publication_date': publication_date,
                'category': category,
                'content': content
            }
        except Exception as e:
            logger.error(f"Error extracting article data: {str(e)}")
            return None

    def parse_date(self, date_str: str) -> datetime:
        """Parse date with multiple format support"""
        if not date_str:
            return datetime.now()
            
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%B %d, %Y",
            "%d %B %Y",
            "%Y-%m-%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        logger.warning(f"Could not parse date: {date_str}")
        return datetime.now()

    async def scrape_page(self, session: aiohttp.ClientSession, page_url: str) -> List[Dict]:
        """Scrape articles from a single page"""
        html = await self.fetch_page(session, page_url)
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # TheSaaSNews-specific article selectors
        article_elements = soup.find_all('article') or soup.find_all(class_='post')
        
        for element in article_elements:
            article_data = self.extract_article_data(element, self.base_url)
            if article_data and article_data['url']:
                articles.append(article_data)
                
        return articles

    async def get_pagination_urls(self, session: aiohttp.ClientSession, start_url: str, max_pages: int = 5) -> List[str]:
        """Get all pagination URLs"""
        urls = [start_url]
        current_url = start_url
        
        for page_num in range(2, max_pages + 1):
            html = await self.fetch_page(session, current_url)
            if not html:
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for next page link
            next_link = soup.find('a', class_='next') or soup.find('a', string='Next')
            if next_link and next_link.get('href'):
                next_url = urljoin(self.base_url, next_link['href'])
                urls.append(next_url)
                current_url = next_url
            else:
                # Try page number approach
                page_url = f"{start_url}/page/{page_num}/"
                urls.append(page_url)
                
        return urls

    async def scrape_all_pages(self, max_pages: int = 5) -> List[Dict]:
        """Scrape articles from multiple pages with pagination"""
        all_articles = []
        
        async with aiohttp.ClientSession() as session:
            start_url = f"{self.base_url}/news/"  # Adjust based on actual site structure
            page_urls = await self.get_pagination_urls(session, start_url, max_pages)
            
            # Concurrent scraping of multiple pages
            tasks = [self.scrape_page(session, url) for url in page_urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_articles.extend(result)
                else:
                    logger.error(f"Scraping error: {result}")
                    
        logger.info(f"Scraped {len(all_articles)} articles from {len(page_urls)} pages")
        return all_articles
