#!/usr/bin/env python3
"""Build comprehensive diocese list from GCatholic.org."""
import requests
from bs4 import BeautifulSoup
import json
import time


def fetch_usa_dioceses():
    """Fetch all U.S. dioceses from GCatholic."""
    print("🌍 Fetching U.S. dioceses from GCatholic.org...")
    
    url = "https://www.gcat holic.org/dioceses/country/US.htm"
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'CatholicMassFinderBot/1.0 (Educational Project)'})
    
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        dioceses = []
        
        # Find all diocese links
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().strip()
            
            # Look for diocese/archdiocese links
            if 'diocese' in href.lower() and text:
                # Try to extract state from text (usually in parentheses)
                state = None
                if '(' in text and ')' in text:
                    state_part = text[text.rfind('('):text.rfind(')')+1]
                    # Extract state abbreviation
                    import re
                    state_match = re.search(r'\\b([A-Z]{2})\\b', state_part)
                    if state_match:
                        state = state_match.group(1)
                
                diocese_name = text.replace(f'({state})' if state else '', '').strip()
                
                # Build diocese URL (attempt common patterns)
                website = f"https://www.{diocese_name.lower().replace(' ', '').replace('diocese', '').replace('archdiocese', '')}.org"
                
                dioceses.append({
                    'name': diocese_name,
                    'state': state or 'Unknown',
                    'country': 'USA',
                    'website': website,
                    'parishes_page': f"{website}/parishes",
                    'scraper': 'generic'
                })
        
        return dioceses
        
    except Exception as e:
        print(f"❌ Error fetching dioceses: {e}")
        return []


def main():
    """Main function."""
    print("🏛️  Building Diocese List")
    print("=" * 60)
    
    # For now, let's use a curated list of major U.S. dioceses
    # This is more reliable than scraping GCatholic dynamically
    
    dioceses = [
        # Kentucky (all 4 dioceses)
        {"name": "Diocese of Lexington", "state": "KY", "country": "USA", "website": "https://www.cdlex.org", "parishes_page": "https://www.cdlex.org/parishes", "scraper": "lexington"},
        {"name": "Archdiocese of Louisville", "state": "KY", "country": "USA", "website": "https://www.archlou.org", "parishes_page": "https://www.archlou.org/parishes", "scraper": "generic"},
        {"name": "Diocese of Covington", "state": "KY", "country": "USA", "website": "https://www.covdio.org", "parishes_page": "https://www.covdio.org/parishes", "scraper": "generic"},
        {"name": "Diocese of Owensboro", "state": "KY", "country": "USA", "website": "https://www.pastoral.org", "parishes_page": "https://www.pastoral.org/parishes", "scraper": "generic"},
        
        # Major U.S. Archdioceses
        {"name": "Archdiocese of New York", "state": "NY", "country": "USA", "website": "https://www.archny.org", "parishes_page": "https://www.archny.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Los Angeles", "state": "CA", "country": "USA", "website": "https://lacatholics.org", "parishes_page": "https://lacatholics.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Chicago", "state": "IL", "country": "USA", "website": "https://www.archchicago.org", "parishes_page": "https://www.archchicago.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Boston", "state": "MA", "country": "USA", "website": "https://www.bostoncatholic.org", "parishes_page": "https://www.bostoncatholic.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Philadelphia", "state": "PA", "country": "USA", "website": "https://www.archphila.org", "parishes_page": "https://www.archphila.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Detroit", "state": "MI", "country": "USA", "website": "https://www.aod.org", "parishes_page": "https://www.aod.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Miami", "state": "FL", "country": "USA", "website": "https://www.miamiarch.org", "parishes_page": "https://www.miamiarch.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Atlanta", "state": "GA", "country": "USA", "website": "https://www.archatl.com", "parishes_page": "https://www.archatl.com/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Seattle", "state": "WA", "country": "USA", "website": "https://www.seattlearch.org", "parishes_page": "https://www.seattlearch.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Denver", "state": "CO", "country": "USA", "website": "https://www.archden.org", "parishes_page": "https://www.archden.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of San Francisco", "state": "CA", "country": "USA", "website": "https://www.sfarch.org", "parishes_page": "https://www.sfarch.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Baltimore", "state": "MD", "country": "USA", "website": "https://www.archbalt.org", "parishes_page": "https://www.archbalt.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Washington", "state": "DC", "country": "USA", "website": "https://www.adw.org", "parishes_page": "https://www.adw.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of Galveston-Houston", "state": "TX", "country": "USA", "website": "https://www.archgh.org", "parishes_page": "https://www.archgh.org/parishes", "scraper": "generic"},
        {"name": "Archdiocese of San Antonio", "state": "TX", "country": "USA", "website": "https://www.archsa.org", "parishes_page": "https://www.archsa.org/parishes", "scraper": "generic"},
    ]
    
    print(f"✅ Built list of {len(dioceses)} dioceses")
    
    # Write to config.py
    with open('config.py', 'w') as f:
        f.write('"""Configuration for diocese scrapers."""\n\n')
        f.write('DIOCESES = [\n')
        for d in dioceses:
            f.write(f'    {d},\n')
        f.write(']\n')
    
    print("💾 Saved to config.py")
    

if __name__ == '__main__':
    main()
