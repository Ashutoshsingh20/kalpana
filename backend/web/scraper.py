"""
Kalpana AGI - Web Scraper Module
Purpose: Extract and clean web content for research and analysis.
Dependencies: playwright, beautifulsoup4
"""

import logging
from bs4 import BeautifulSoup
from typing import Dict, List, Any
from backend.web.browser_automation import browser_automation

logger = logging.getLogger("Kalpana.WebScraper")

class WebScraper:
    async def scrape_url(self, url: str) -> Dict[str, Any]:
        """
        Scrape a URL and return structured data.
        """
        try:
            logger.info(f"Scraping: {url}")
            
            # Navigate to URL
            success = await browser_automation.navigate(url)
            if not success:
                return {"error": "Failed to load page"}
            
            # Get page info
            page_info = await browser_automation.get_page_info()
            
            # Get page HTML
            html = await browser_automation.get_text()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract structured data
            title = page_info.get("title", "")
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Extract headings
            headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    links.append({"text": link.get_text().strip(), "url": href})
            
            result = {
                "url": page_info.get("url", url),
                "title": title,
                "content": text[:5000],  # Limit to 5000 chars
                "headings": headings[:10],
                "links": links[:20],
                "success": True
            }
            
            logger.info(f"Scraped {len(text)} characters from {url}")
            return result
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return {"error": str(e), "success": False}
    
    async def research(self, query: str) -> str:
        """
        Research a topic by scraping Google search results.
        """
        try:
            # Use DuckDuckGo for privacy (or Google)
            search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            result = await self.scrape_url(search_url)
            
            if not result.get("success"):
                return f"Failed to research '{query}': {result.get('error')}"
            
            # Extract summary
            content = result.get("content", "")
            title = result.get("title", "")
            
            summary = f"Research on '{query}':\n\n"
            summary += f"Source: {search_url}\n\n"
            summary += f"{content[:1000]}..."  # First 1000 chars
            
            return summary
            
        except Exception as e:
            logger.error(f"Research error: {e}")
            return f"Research failed: {str(e)}"

web_scraper = WebScraper()
