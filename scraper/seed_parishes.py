#!/usr/bin/env python3
"""Seed database with known Kentucky parishes for testing."""
from database import ParishDatabase
from geocoder import Geocoder


def main():
    """Seed parishes."""
    print("🌱 Seeding database with Kentucky parishes...")
    
    # Known Kentucky parishes with addresses
    parishes = [
        {
            "name": "St. Martha Catholic Church",
            "diocese": "Diocese of Lexington",
            "street": "214 S Lake Dr",
            "city": "Prestonsburg",
            "state": "KY",
            "zip": "41653",
            "address": "214 S Lake Dr, Prestonsburg, KY 41653",
            "phone": "(606) 886-2390",
            "country": "United States"
        },
        {
            "name": "Cathedral of Christ the King",
            "diocese": "Diocese of Lexington",
            "street": "299 Colony Blvd",
            "city": "Lexington",
            "state": "KY",
            "zip": "40502",
            "address": "299 Colony Blvd, Lexington, KY 40502",
            "phone": "(859) 268-1537",
            "website": "https://www.ccaking.org",
            "country": "United States"
        },
        {
            "name": "St. Peter Catholic Church",
            "diocese": "Diocese of Lexington",
            "street": "105 N Main St",
            "city": "Lexington",
            "state": "KY",
            "zip": "40507",
            "address": "105 N Main St, Lexington, KY 40507",
            "phone": "(859) 252-0125",
            "country": "United States"
        },
        {
            "name": "Cathedral of the Assumption",
            "diocese": "Archdiocese of Louisville",
            "street": "433 S 5th St",
            "city": "Louisville",
            "state": "KY",
            "zip": "40202",
            "address": "433 S 5th St, Louisville, KY 40202",
            "phone": "(502) 582-2971",
            "website": "https://www.cathedraloftheassumption.org",
            "country": "United States"
        },
        {
            "name": "St. Patrick Catholic Church",
            "diocese": "Diocese of Covington",
            "street": "310 13th St",
            "city": "Newport",
            "state": "KY",
            "zip": "41071",
            "address": "310 13th St, Newport, KY 41071",
            "phone": "(859) 291-2288",
            "country": "United States"
        },
        {
            "name": "St. Stephen Cathedral",
            "diocese": "Diocese of Owensboro",
            "street": "610 Locust St",
            "city": "Owensboro",
            "state": "KY",
            "zip": "42301",
            "address": "610 Locust St, Owensboro, KY 42301",
            "phone": "(270) 683-3606",
            "country": "United States"
        },
    ]
    
    geocoder = Geocoder()
    
    with ParishDatabase("parishes.db") as db:
        # Clear existing data
        db.cursor.execute("DELETE FROM parishes")
        db.cursor.execute("DELETE FROM scrape_log")
        db.conn.commit()
        print("🗑️  Cleared existing data")
        
        # Insert parishes with geocoding
        for parish in parishes:
            print(f"\\n📍 {parish['name']}")
            
            # Geocode
            coords = geocoder.geocode(
                parish['address'],
                parish['city'],
                parish['state'],
                parish['zip']
            )
            
            if coords:
                parish['latitude'], parish['longitude'] = coords
                print(f"   ✓ Geocoded: {coords}")
            else:
                print(f"   ✗ Could not geocode")
                
            # Insert
            parish_id = db.insert_parish(parish)
            print(f"   ✓ Saved to database (ID: {parish_id})")
            
        # Print stats
        stats = db.get_stats()
        print("\\n" + "="*60)
        print("📊 Database Statistics")
        print("="*60)
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        print("\\n✅ Seeding complete!")
        

if __name__ == '__main__':
    main()
