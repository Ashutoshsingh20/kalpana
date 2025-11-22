"""
Kalpana AGI - Web Search Module
Purpose: Wrapper for web search using DuckDuckGo and Bing APIs.
Dependencies: requests, beautifulsoup4
"""

import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import os

logger = logging.getLogger("Kalpana.WebSearch")

class WebSearch:
    def __init__(self):
        self.bing_api_key = os.getenv("BING_API_KEY", "")
        self.use_bing = bool(self.bing_api_key)
    
    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search DuckDuckGo and return top results.
        """
        try:
            search_url = f"https://duckduckgo.com/html/?q={query.replace(' ', '+')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result'):
                if len(results) >= max_results:
                    break
                
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')
                
                if title_elem:
                    title = title_elem.get_text().strip()
                    url = title_elem.get('href', '')
                    snippet = snippet_elem.get_text().strip() if snippet_elem else ""
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
            
            logger.info(f"DuckDuckGo search for '{query}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []
    
    def search_bing(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using Bing API and return top results.
        """
        if not self.use_bing:
            logger.warning("Bing API key not configured")
            return []
        
        try:
            endpoint = "https://api.bing.microsoft.com/v7.0/search"
            headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
            params = {'q': query, 'count': max_results}
            
            response = requests.get(endpoint, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('webPages', {}).get('value', []):
                results.append({
                    'title': item.get('name', ''),
                    'url': item.get('url', ''),
                    'snippet': item.get('snippet', '')
                })
            
            logger.info(f"Bing search for '{query}' returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Bing search error: {e}")
            return []
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Search using the best available method.
        """
        if self.use_bing:
            return self.search_bing(query, max_results)
        else:
            return self.search_duckduckgo(query, max_results)

web_search = WebSearch()
