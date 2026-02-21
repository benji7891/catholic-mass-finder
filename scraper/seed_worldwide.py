#!/usr/bin/env python3
"""Seed database with parishes from major cities worldwide."""
from database import ParishDatabase

def main():
    """Seed parishes from around the world."""
    print("🌍 Seeding worldwide parishes...")
    
    # Major parishes from around the world with known coordinates
    parishes = [
        # United States - Kentucky
        {"name": "St. Martha Catholic Church", "diocese": "Diocese of Lexington", "street": "214 S Lake Dr", "city": "Prestonsburg", "state": "KY", "zip": "41653", "address": "214 S Lake Dr, Prestonsburg, KY 41653", "phone": "(606) 886-2390", "country": "United States", "latitude": 37.6642, "longitude": -82.7718},
        {"name": "Cathedral of Christ the King", "diocese": "Diocese of Lexington", "street": "299 Colony Blvd", "city": "Lexington", "state": "KY", "zip": "40502", "address": "299 Colony Blvd, Lexington, KY 40502", "phone": "(859) 268-1537", "website": "https://www.ccaking.org", "country": "United States", "latitude": 38.0408, "longitude": -84.4733},
        {"name": "St. Peter Catholic Church", "diocese": "Diocese of Lexington", "street": "105 N Main St", "city": "Lexington", "state": "KY", "zip": "40507", "address": "105 N Main St, Lexington, KY 40507", "phone": "(859) 252-0125", "country": "United States", "latitude": 38.0373, "longitude": -84.4947},
        {"name": "Cathedral of the Assumption", "diocese": "Archdiocese of Louisville", "street": "433 S 5th St", "city": "Louisville", "state": "KY", "zip": "40202", "address": "433 S 5th St, Louisville, KY 40202", "phone": "(502) 582-2971", "website": "https://www.cathedraloftheassumption.org", "country": "United States", "latitude": 38.2542, "longitude": -85.7585},
        {"name": "St. Patrick Catholic Church", "diocese": "Diocese of Covington", "street": "310 13th St", "city": "Newport", "state": "KY", "zip": "41071", "address": "310 13th St, Newport, KY 41071", "phone": "(859) 291-2288", "country": "United States", "latitude": 39.0881, "longitude": -84.4947},
        {"name": "St. Stephen Cathedral", "diocese": "Diocese of Owensboro", "street": "610 Locust St", "city": "Owensboro", "state": "KY", "zip": "42301", "address": "610 Locust St, Owensboro, KY 42301", "phone": "(270) 683-3606", "country": "United States", "latitude": 37.7742, "longitude": -87.1112},
        
        # New York
        {"name": "St. Patrick's Cathedral", "diocese": "Archdiocese of New York", "street": "5th Ave", "city": "New York", "state": "NY", "zip": "10022", "address": "5th Ave, New York, NY 10022", "phone": "(212) 753-2261", "website": "https://www.saintpatrickscathedral.org", "country": "United States", "latitude": 40.7585, "longitude": -73.9760},
        {"name": "Cathedral of St. John the Divine", "diocese": "Archdiocese of New York", "street": "1047 Amsterdam Ave", "city": "New York", "state": "NY", "zip": "10025", "address": "1047 Amsterdam Ave, New York, NY 10025", "country": "United States", "latitude": 40.8041, "longitude": -73.9621},
        
        # California
        {"name": "Cathedral of Our Lady of the Angels", "diocese": "Archdiocese of Los Angeles", "street": "555 W Temple St", "city": "Los Angeles", "state": "CA", "zip": "90012", "address": "555 W Temple St, Los Angeles, CA 90012", "phone": "(213) 680-5200", "country": "United States", "latitude": 34.0577, "longitude": -118.2459},
        {"name": "Mission Dolores Basilica", "diocese": "Archdiocese of San Francisco", "street": "3321 16th St", "city": "San Francisco", "state": "CA", "zip": "94114", "address": "3321 16th St, San Francisco, CA 94114", "country": "United States", "latitude": 37.7644, "longitude": -122.4262},
        
        # Texas
        {"name": "Co-Cathedral of the Sacred Heart", "diocese": "Archdiocese of Galveston-Houston", "street": "1111 St Joseph Pkwy", "city": "Houston", "state": "TX", "zip": "77002", "address": "1111 St Joseph Pkwy, Houston, TX 77002", "country": "United States", "latitude": 29.7516, "longitude": -95.3635},
        {"name": "San Fernando Cathedral", "diocese": "Archdiocese of San Antonio", "street": "115 Main Plaza", "city": "San Antonio", "state": "TX", "zip": "78205", "address": "115 Main Plaza, San Antonio, TX 78205", "country": "United States", "latitude": 29.4251, "longitude": -98.4936},
        
        # International - Major Cities
        # Canada
        {"name": "Notre-Dame Basilica", "diocese": "Archdiocese of Montreal", "city": "Montreal", "state": "QC", "country": "Canada", "latitude": 45.5045, "longitude": -73.5565, "address": "110 Notre-Dame St W, Montreal, QC, Canada"},
        {"name": "St. Michael's Cathedral Basilica", "diocese": "Archdiocese of Toronto", "city": "Toronto", "state": "ON", "country": "Canada", "latitude": 43.6543, "longitude": -79.3763, "address": "65 Bond St, Toronto, ON, Canada"},
        
        # United Kingdom
        {"name": "Westminster Cathedral", "diocese": "Archdiocese of Westminster", "city": "London", "state": "", "country": "United Kingdom", "latitude": 51.4958, "longitude": -0.1394, "address": "42 Francis St, Westminster, London, UK"},
        {"name": "St. Mary's Cathedral", "diocese": "Archdiocese of Edinburgh", "city": "Edinburgh", "state": "", "country": "United Kingdom", "latitude": 55.9466, "longitude": -3.2063, "address": "61 York Pl, Edinburgh, UK"},
        
        # Ireland
        {"name": "Pro-Cathedral", "diocese": "Archdiocese of Dublin", "city": "Dublin", "state": "", "country": "Ireland", "latitude": 53.3515, "longitude": -6.2572, "address": "83 Marlborough St, Dublin, Ireland"},
        
        # France
        {"name": "Notre-Dame de Paris", "diocese": "Archdiocese of Paris", "city": "Paris", "state": "", "country": "France", "latitude": 48.8530, "longitude": 2.3499, "address": "6 Parvis Notre-Dame, Paris, France"},
        {"name": "Sacré-Cœur", "diocese": "Archdiocese of Paris", "city": "Paris", "state": "", "country": "France", "latitude": 48.8867, "longitude": 2.3431, "address": "35 Rue du Chevalier de la Barre, Paris, France"},
        
        # Italy
        {"name": "St. Peter's Basilica", "diocese": "Diocese of Rome", "city": "Vatican City", "state": "", "country": "Vatican City", "latitude": 41.9022, "longitude": 12.4539, "address": "Piazza San Pietro, Vatican City"},
        {"name": "Duomo di Milano", "diocese": "Archdiocese of Milan", "city": "Milan", "state": "", "country": "Italy", "latitude": 45.4642, "longitude": 9.1900, "address": "Piazza del Duomo, Milan, Italy"},
        
        # Spain
        {"name": "Sagrada Família", "diocese": "Archdiocese of Barcelona", "city": "Barcelona", "state": "", "country": "Spain", "latitude": 41.4036, "longitude": 2.1744, "address": "Carrer de Mallorca, 401, Barcelona, Spain"},
        {"name": "Cathedral of Santiago de Compostela", "diocese": "Archdiocese of Santiago de Compostela", "city": "Santiago de Compostela", "state": "", "country": "Spain", "latitude": 42.8805, "longitude": -8.5448, "address": "Praza do Obradoiro, Santiago de Compostela, Spain"},
        
        # Germany
        {"name": "Cologne Cathedral", "diocese": "Archdiocese of Cologne", "city": "Cologne", "state": "", "country": "Germany", "latitude": 50.9413, "longitude": 6.9583, "address": "Domkloster 4, Cologne, Germany"},
        
        # Poland
        {"name": "St. Mary's Basilica", "diocese": "Archdiocese of Kraków", "city": "Kraków", "state": "", "country": "Poland", "latitude": 50.0619, "longitude": 19.9381, "address": "Plac Mariacki 5, Kraków, Poland"},
        
        # Australia
        {"name": "St. Mary's Cathedral", "diocese": "Archdiocese of Sydney", "city": "Sydney", "state": "NSW", "country": "Australia", "latitude": -33.8713, "longitude": 151.2135, "address": "St Marys Rd, Sydney NSW, Australia"},
        {"name": "St. Patrick's Cathedral", "diocese": "Archdiocese of Melbourne", "city": "Melbourne", "state": "VIC", "country": "Australia", "latitude": -37.8103, "longitude": 144.9676, "address": "1 Cathedral Pl, East Melbourne VIC, Australia"},
        
        # Philippines
        {"name": "Manila Cathedral", "diocese": "Archdiocese of Manila", "city": "Manila", "state": "", "country": "Philippines", "latitude": 14.5926, "longitude": 120.9738, "address": "Cabildo St, Intramuros, Manila, Philippines"},
        
        # Mexico
        {"name": "Metropolitan Cathedral", "diocese": "Archdiocese of Mexico City", "city": "Mexico City", "state": "", "country": "Mexico", "latitude": 19.4348, "longitude": -99.1332, "address": "Plaza de la Constitución, Centro, Mexico City, Mexico"},
        
        # Brazil
        {"name": "Catedral Metropolitana", "diocese": "Archdiocese of São Paulo", "city": "São Paulo", "state": "SP", "country": "Brazil", "latitude": -23.5505, "longitude": -46.6333, "address": "Praça da Sé, São Paulo, SP, Brazil"},
        
        # Argentina
        {"name": "Buenos Aires Metropolitan Cathedral", "diocese": "Archdiocese of Buenos Aires", "city": "Buenos Aires", "state": "", "country": "Argentina", "latitude": -34.6076, "longitude": -58.3738, "address": "San Martín 27, Buenos Aires, Argentina"},
    ]
    
    with ParishDatabase("parishes.db") as db:
        # Clear existing data
        db.cursor.execute("DELETE FROM parishes")
        db.cursor.execute("DELETE FROM scrape_log")
        db.conn.commit()
        print("🗑️  Cleared existing data")
        
        # Insert parishes
        for parish in parishes:
            parish_id = db.insert_parish(parish)
            print(f"  ✓ {parish['name']}, {parish.get('city', 'N/A')}, {parish['country']}")
            
        # Print stats
        stats = db.get_stats()
        print("\n" + "="*60)
        print("📊 Database Statistics")
        print("="*60)
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        print(f"\n✅ Seeded {len(parishes)} parishes from around the world!")

if __name__ == '__main__':
    main()

# Add more Philippine parishes
def add_philippines_parishes():
    """Add more Philippine parishes including Cagayan Valley region."""
    from database import ParishDatabase
    
    new_parishes = [
        # Cagayan Valley Region
        {"name": "San Matthias Parish Church", "diocese": "Diocese of Ilagan", "city": "Tumauini", "state": "Isabela", "country": "Philippines", "latitude": 17.2686, "longitude": 121.7994, "address": "Tumauini, Isabela, Philippines"},
        {"name": "Our Lady of the Pillar Cathedral", "diocese": "Diocese of Ilagan", "city": "Ilagan", "state": "Isabela", "country": "Philippines", "latitude": 17.1453, "longitude": 121.8840, "address": "Ilagan, Isabela, Philippines"},
        {"name": "St. Dominic Cathedral", "diocese": "Diocese of Bayombong", "city": "Bayombong", "state": "Nueva Vizcaya", "country": "Philippines", "latitude": 16.4836, "longitude": 121.1504, "address": "Bayombong, Nueva Vizcaya, Philippines"},
        
        # More major Philippine cities
        {"name": "Quiapo Church", "diocese": "Archdiocese of Manila", "city": "Manila", "state": "", "country": "Philippines", "latitude": 14.5988, "longitude": 120.9826, "address": "Plaza Miranda, Quiapo, Manila, Philippines"},
        {"name": "Cebu Metropolitan Cathedral", "diocese": "Archdiocese of Cebu", "city": "Cebu City", "state": "Cebu", "country": "Philippines", "latitude": 10.2935, "longitude": 123.9015, "address": "Cebu City, Cebu, Philippines"},
        {"name": "San Agustin Church", "diocese": "Archdiocese of Manila", "city": "Manila", "state": "", "country": "Philippines", "latitude": 14.5887, "longitude": 120.9753, "address": "Intramuros, Manila, Philippines"},
        {"name": "Baclaran Church", "diocese": "Archdiocese of Manila", "city": "Parañaque", "state": "", "country": "Philippines", "latitude": 14.4629, "longitude": 121.0115, "address": "Baclaran, Parañaque, Philippines"},
        {"name": "Antipolo Cathedral", "diocese": "Diocese of Antipolo", "city": "Antipolo", "state": "Rizal", "country": "Philippines", "latitude": 14.5868, "longitude": 121.1755, "address": "Antipolo, Rizal, Philippines"},
    ]
    
    with ParishDatabase("parishes.db") as db:
        for parish in new_parishes:
            if not db.parish_exists(parish['name'], parish.get('diocese', 'Unknown')):
                parish_id = db.insert_parish(parish)
                print(f"  ✓ Added: {parish['name']}, {parish['city']}")
            else:
                print(f"  ⏭️  Already exists: {parish['name']}")
        
        stats = db.get_stats()
        print(f"\n📊 Updated stats: {stats['total_parishes']} parishes")

if __name__ == '__main__':
    print("\n🇵🇭 Adding more Philippine parishes...")
    add_philippines_parishes()
