"""Base scraper with generic logic for diocese websites."""
import requests
from bs4 import BeautifulSoup
import re
import time
from typing import List, Dict, Optional


class BaseScraper:
    """Base scraper class with common functionality."""
    
    def __init__(self, diocese_name: str, diocese_state: str):
        """Initialize scraper."""
        self.diocese_name = diocese_name
        self.diocese_state = diocese_state
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CatholicMassFinderBot/1.0 (Educational Project)'
        })
        
    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage."""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Retry {attempt + 1}/{max_retries} for {url}")
                    time.sleep(2)
                else:
                    print(f"❌ Failed to fetch {url}: {e}")
                    return None
        return None
        
    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text."""
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890 or 123-456-7890
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',  # 123.456.7890
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None
        
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email from text."""
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
        
    def extract_zip(self, text: str) -> Optional[str]:
        """Extract ZIP code from text."""
        zip_pattern = r'\b\d{5}(?:-\d{4})?\b'
        match = re.search(zip_pattern, text)
        return match.group(0) if match else None
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
        
    def parse_address(self, address_text: str) -> Dict[str, str]:
        """
        Parse address text into components.
        
        Args:
            address_text: Full address string
            
        Returns:
            Dictionary with address, city, state, zip
        """
        address_text = self.clean_text(address_text)
        
        result = {
            'address': address_text,
            'street': None,
            'city': None,
            'state': self.diocese_state,
            'zip': None
        }
        
        # Extract ZIP code
        zip_code = self.extract_zip(address_text)
        if zip_code:
            result['zip'] = zip_code
            
        # Try to parse city, state, ZIP pattern
        # Example: "123 Main St, Lexington, KY 40503"
        parts = address_text.split(',')
        if len(parts) >= 3:
            result['street'] = parts[0].strip()
            result['city'] = parts[1].strip()
            # Last part might have state and ZIP
            last_part = parts[-1].strip()
            state_match = re.search(r'\b[A-Z]{2}\b', last_part)
            if state_match:
                result['state'] = state_match.group(0)
        elif len(parts) == 2:
            result['street'] = parts[0].strip()
            result['city'] = parts[1].strip()
            
        return result
        
    def find_parish_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Find all parish detail page links.
        
        Args:
            soup: BeautifulSoup object of parishes listing page
            base_url: Base URL for relative links
            
        Returns:
            List of parish detail page URLs
        """
        parish_links = []
        
        # Look for links with parish-related keywords
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().lower()
            
            # Check if link looks like a parish detail page
            if any(keyword in href.lower() or keyword in text for keyword in 
                   ['parish', 'church', 'catholic']):
                # Convert relative to absolute URL
                if href.startswith('http'):
                    parish_links.append(href)
                elif href.startswith('/'):
                    parish_links.append(base_url.rstrip('/') + href)
                    
        return list(set(parish_links))  # Remove duplicates
        
    def scrape_parish_list(self, parishes_url: str) -> List[Dict]:
        """
        Generic scraper for parish listing page.
        Should be overridden by custom scrapers for specific dioceses.
        
        Args:
            parishes_url: URL of the parishes listing page
            
        Returns:
            List of parish data dictionaries
        """
        raise NotImplementedError("Subclasses must implement scrape_parish_list")
