"""
Kalpana AGI - Browser Automation Module
Purpose: Playwright wrapper for web interaction and automation.
Dependencies: playwright
Permissions: Network Access
"""

import asyncio
import logging
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from typing import Optional, Dict, Any

logger = logging.getLogger("Kalpana.BrowserAutomation")

class BrowserAutomation:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    async def initialize(self):
        """Initialize Playwright browser instance."""
        if self.browser:
            logger.warning("Browser already initialized")
            return
            
        logger.info("Initializing Playwright browser...")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        self.page = await self.context.new_page()
        logger.info("Browser initialized successfully")
    
    async def navigate(self, url: str, wait_until: str = "networkidle") -> bool:
        """Navigate to a URL."""
        try:
            if not self.page:
                await self.initialize()
            
            logger.info(f"Navigating to: {url}")
            await self.page.goto(url, wait_until=wait_until)
            return True
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return False
    
    async def get_text(self, selector: Optional[str] = None) -> str:
        """Extract text from page or specific element."""
        try:
            if not self.page:
                return ""
            
            if selector:
                element = await self.page.query_selector(selector)
                if element:
                    return await element.inner_text()
                return ""
            else:
                return await self.page.inner_text("body")
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return ""
    
    async def click(self, selector: str) -> bool:
        """Click an element."""
        try:
            if not self.page:
                return False
            
            await self.page.click(selector)
            return True
        except Exception as e:
            logger.error(f"Click error: {e}")
            return False
    
    async def fill(self, selector: str, text: str) -> bool:
        """Fill a form field."""
        try:
            if not self.page:
                return False
            
            await self.page.fill(selector, text)
            return True
        except Exception as e:
            logger.error(f"Fill error: {e}")
            return False
    
    async def screenshot(self, path: str) -> bool:
        """Take a screenshot."""
        try:
            if not self.page:
                return False
            
            await self.page.screenshot(path=path)
            logger.info(f"Screenshot saved: {path}")
            return True
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return False
    
    async def get_page_info(self) -> Dict[str, Any]:
        """Get current page information."""
        try:
            if not self.page:
                return {}
            
            title = await self.page.title()
            url = self.page.url
            
            return {"title": title, "url": url}
        except Exception as e:
            logger.error(f"Page info error: {e}")
            return {}
    
    async def close(self):
        """Close browser and cleanup."""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None
            
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Close error: {e}")

# Global instance
browser_automation = BrowserAutomation(headless=True)
