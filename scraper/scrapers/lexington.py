"""Custom scraper for Diocese of Lexington."""
from typing import List, Dict
from .base_scraper import BaseScraper
import time


class LexingtonScraper(BaseScraper):
    """Scraper for Diocese of Lexington parishes."""
    
    def scrape_parish_list(self, parishes_url: str) -> List[Dict]:
        """
        Scrape Diocese of Lexington parishes.
        
        Args:
            parishes_url: URL of parishes page (https://www.cdlex.org/parishes)
            
        Returns:
            List of parish dictionaries with name, address, phone, etc.
        """
        print(f"🔍 Scraping {self.diocese_name}...")
        
        soup = self.fetch_page(parishes_url)
        if not soup:
            return []
            
        parishes = []
        
        # Look for parish listings - trying multiple approaches
        # Approach 1: Look for divs or sections with parish class
        parish_containers = soup.find_all(['div', 'article', 'section'], 
                                         class_=lambda x: x and ('parish' in x.lower() or 'church' in x.lower()))
        
        if not parish_containers:
            # Approach 2: Look for lists or tables
            parish_containers = soup.find_all(['li', 'tr'], 
                                             class_=lambda x: x and ('parish' in x.lower() or 'church' in x.lower()))
        
        if not parish_containers:
            # Approach 3: Find all links that mention parishes and scrape each
            parish_links = self.find_parish_links(soup, parishes_url)
            print(f"📋 Found {len(parish_links)} parish links to scrape")
            
            for link in parish_links[:10]:  # Limit to 10 for testing
                parish_data = self.scrape_parish_detail(link)
                if parish_data:
                    parishes.append(parish_data)
                time.sleep(2)  # Be polite
                
            return parishes
        
        # Process parish containers
        print(f"📋 Found {len(parish_containers)} parishes")
        
        for container in parish_containers:
            parish_data = self.extract_parish_from_container(container, parishes_url)
            if parish_data:
                parishes.append(parish_data)
                
        return parishes
        
    def extract_parish_from_container(self, container, source_url: str) -> Dict:
        """Extract parish data from a container element."""
        parish_data = {
            'diocese': self.diocese_name,
            'state': self.diocese_state,
            'source_url': source_url
        }
        
        # Extract parish name (usually in h2, h3, or strong tag)
        name_tag = container.find(['h2', 'h3', 'h4', 'strong', 'a'])
        if name_tag:
            parish_data['name'] = self.clean_text(name_tag.get_text())
        else:
            return None  # Can't use parish without name
            
        # Extract all text and parse for address, phone, email
        text = container.get_text()
        
        # Extract phone
        phone = self.extract_phone(text)
        if phone:
            parish_data['phone'] = phone
            
        # Extract email
        email = self.extract_email(text)
        if email:
            parish_data['email'] = email
            
        # Extract website
        website_link = container.find('a', href=lambda x: x and ('http' in x or 'www' in x))
        if website_link and website_link.get('href'):
            href = website_link['href']
            if href.startswith('http'):
                parish_data['website'] = href
                
        # Try to find address
        # Look for address tag or text patterns
        address_tag = container.find(['address', 'p'], 
                                     class_=lambda x: x and 'address' in x.lower() if x else False)
        if address_tag:
            address_text = self.clean_text(address_tag.get_text())
            addr_parts = self.parse_address(address_text)
            parish_data.update(addr_parts)
        else:
            # Try to extract from all text
            lines = [self.clean_text(line) for line in text.split('\n') if line.strip()]
            for line in lines:
                # Look for lines that look like addresses (contain numbers and commas)
                if any(char.isdigit() for char in line) and ',' in line:
                    addr_parts = self.parse_address(line)
                    parish_data.update(addr_parts)
                    break
                    
        return parish_data
        
    def scrape_parish_detail(self, url: str) -> Dict:
        """Scrape individual parish detail page."""
        print(f"  📄 Scraping {url}")
        
        soup = self.fetch_page(url)
        if not soup:
            return None
            
        parish_data = {
            'diocese': self.diocese_name,
            'state': self.diocese_state,
            'source_url': url
        }
        
        # Extract parish name from title or h1
        name_tag = soup.find(['h1', 'h2', 'title'])
        if name_tag:
            name = self.clean_text(name_tag.get_text())
            # Remove common suffixes
            name = name.replace(' - Diocese of Lexington', '').replace(' | Diocese of Lexington', '')
            parish_data['name'] = name
        else:
            return None
            
        # Get main content area
        main_content = soup.find(['main', 'article', 'div'], 
                                class_=lambda x: x and 'content' in x.lower() if x else False)
        if not main_content:
            main_content = soup
            
        text = main_content.get_text()
        
        # Extract contact info
        phone = self.extract_phone(text)
        if phone:
            parish_data['phone'] = phone
            
        email = self.extract_email(text)
        if email:
            parish_data['email'] = email
            
        # Extract website
        website_link = main_content.find('a', href=lambda x: x and 'parish' in x.lower() and x.startswith('http'))
        if website_link:
            parish_data['website'] = website_link['href']
            
        # Extract address
        address_tag = main_content.find('address')
        if address_tag:
            address_text = self.clean_text(address_tag.get_text())
            addr_parts = self.parse_address(address_text)
            parish_data.update(addr_parts)
        else:
            # Look through text for address-like patterns
            lines = [self.clean_text(line) for line in text.split('\n') if line.strip()]
            for i, line in enumerate(lines):
                if any(char.isdigit() for char in line) and ('street' in line.lower() or 'st' in line.lower() or 'road' in line.lower() or 'rd' in line.lower()):
                    # Combine this line and next few lines for full address
                    address_text = ' '.join(lines[i:min(i+3, len(lines))])
                    addr_parts = self.parse_address(address_text)
                    parish_data.update(addr_parts)
                    break
                    
        # Extract mass times if available
        mass_section = main_content.find(['div', 'section'], 
                                        class_=lambda x: x and ('mass' in x.lower() or 'schedule' in x.lower()) if x else False)
        if mass_section:
            parish_data['mass_times'] = self.clean_text(mass_section.get_text())
            
        return parish_data
