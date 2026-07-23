import httpx
from bs4 import BeautifulSoup

def scrape_job_description_sync(url: str) -> str:
    """Fetches job description from URL. Uses Playwright for JS sites, falls back to HTTPX."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=15000)
            content = page.content()
            browser.close()
            
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        print(f"Playwright failed: {e}. Falling back to httpx.")
        return fallback_scrape(url)

def fallback_scrape(url: str) -> str:
    try:
        response = httpx.get(url, timeout=10.0)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        return f"Error scraping {url}: {e}"
