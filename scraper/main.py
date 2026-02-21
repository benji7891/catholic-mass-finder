#!/usr/bin/env python3
"""Main entry point for parish scraper."""
import sys
from pathlib import Path
from tqdm import tqdm

from database import ParishDatabase
from geocoder import Geocoder
from config import DIOCESES
from scrapers.lexington import LexingtonScraper


def get_scraper(diocese_config):
    """Get appropriate scraper for diocese."""
    scraper_type = diocese_config.get('scraper', 'generic')
    diocese_name = diocese_config['name']
    diocese_state = diocese_config['state']
    
    if scraper_type == 'lexington':
        return LexingtonScraper(diocese_name, diocese_state)
    else:
        # TODO: Implement generic scraper
        print(f"⚠️  Generic scraper not yet implemented for {diocese_name}")
        return None


def scrape_diocese(diocese_config, db, geocoder):
    """Scrape a single diocese."""
    print(f"\n{'='*60}")
    print(f"📍 {diocese_config['name']} ({diocese_config['state']})")
    print(f"{'='*60}")
    
    # Get scraper
    scraper = get_scraper(diocese_config)
    if not scraper:
        db.log_scrape(diocese_config['name'], 'failed', 0, 'No scraper available')
        return
        
    try:
        # Scrape parishes
        parishes = scraper.scrape_parish_list(diocese_config['parishes_page'])
        
        if not parishes:
            print("❌ No parishes found")
            db.log_scrape(diocese_config['name'], 'failed', 0, 'No parishes found')
            return
            
        print(f"\n✅ Found {len(parishes)} parishes")
        print("\n🌍 Geocoding addresses...")
        
        # Geocode and save parishes
        parishes_saved = 0
        
        for parish in tqdm(parishes, desc="Processing parishes"):
            # Check if parish already exists
            if db.parish_exists(parish['name'], diocese_config['name']):
                print(f"⏭️  Skipping existing: {parish['name']}")
                continue
                
            # Geocode if we have an address
            if parish.get('address'):
                coords = geocoder.geocode(
                    parish.get('address', ''),
                    parish.get('city'),
                    parish.get('state'),
                    parish.get('zip')
                )
                if coords:
                    parish['latitude'], parish['longitude'] = coords
                    print(f"  ✓ {parish['name']}: {coords}")
                else:
                    print(f"  ✗ {parish['name']}: Could not geocode")
                    
            # Save to database
            try:
                db.insert_parish(parish)
                parishes_saved += 1
            except Exception as e:
                print(f"❌ Error saving {parish['name']}: {e}")
                
        # Log scrape result
        db.log_scrape(diocese_config['name'], 'success', parishes_saved)
        print(f"\n✅ Saved {parishes_saved} parishes to database")
        
    except Exception as e:
        print(f"❌ Error scraping {diocese_config['name']}: {e}")
        import traceback
        traceback.print_exc()
        db.log_scrape(diocese_config['name'], 'failed', 0, str(e))


def main():
    """Main function."""
    print("🏛️  Catholic Mass Finder - Parish Scraper")
    print("=" * 60)
    
    # Get database path
    db_path = Path(__file__).parent / "parishes.db"
    print(f"📁 Database: {db_path}")
    
    # Check if database needs initialization
    needs_init = not db_path.exists()
    
    # Initialize database
    with ParishDatabase(str(db_path)) as db:
        # Initialize schema if needed
        if needs_init:
            print("🔨 Initializing database...")
            db.initialize()
        else:
            print("✅ Database exists")
            try:
                stats = db.get_stats()
                print(f"📊 Current stats: {stats['total_parishes']} parishes, "
                      f"{stats['dioceses_scraped']} dioceses, {stats['states_covered']} states")
            except Exception as e:
                print(f"⚠️  Database exists but needs initialization: {e}")
                db.initialize()
            
        # Initialize geocoder
        geocoder = Geocoder()
        
        # Scrape all configured dioceses
        print(f"\n🎯 Scraping {len(DIOCESES)} dioceses...")
        
        for diocese in DIOCESES:
            scrape_diocese(diocese, db, geocoder)
            
        # Print final stats
        print("\n" + "=" * 60)
        print("📊 Final Statistics")
        print("=" * 60)
        stats = db.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        print("\n✅ Scraping complete!")
        print(f"💾 Database saved to: {db_path}")


if __name__ == '__main__':
    main()
