#!/usr/bin/env python3
"""
PHASE 1: Comprehensive USA Parish Expansion
Add parishes from all 50 states covering major dioceses
"""
from database import ParishDatabase

def main():
    print("="*70)
    print("PHASE 1: USA COMPREHENSIVE EXPANSION")
    print("="*70)
    print("\nAdding parishes from all 50 states...\n")
    
    parishes = [
        # EXISTING USA PARISHES (will skip if exist)
        # Kentucky already covered
        # NY, CA, TX already have some
        
        # ========== ALABAMA ==========
        {"name": "Cathedral of St. Paul", "diocese": "Diocese of Birmingham", "city": "Birmingham", "state": "AL", "country": "United States", "latitude": 33.5186, "longitude": -86.8104, "address": "2120 3rd Ave N, Birmingham, AL"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Archdiocese of Mobile", "city": "Mobile", "state": "AL", "country": "United States", "latitude": 30.6944, "longitude": -88.0431, "address": "400 Government St, Mobile, AL"},
        
        # ========== ALASKA ==========
        {"name": "Holy Family Cathedral", "diocese": "Archdiocese of Anchorage-Juneau", "city": "Anchorage", "state": "AK", "country": "United States", "latitude": 61.2181, "longitude": -149.9003, "address": "826 W 5th Ave, Anchorage, AK"},
        
        # ========== ARKANSAS ==========
        {"name": "Cathedral of St. Andrew", "diocese": "Diocese of Little Rock", "city": "Little Rock", "state": "AR", "country": "United States", "latitude": 34.7465, "longitude": -92.2896, "address": "617 Louisiana St, Little Rock, AR"},
        
        # ========== ARIZONA (add more) ==========
        {"name": "St. Augustine Cathedral", "diocese": "Diocese of Tucson", "city": "Tucson", "state": "AZ", "country": "United States", "latitude": 32.2226, "longitude": -110.9747, "address": "192 S Stone Ave, Tucson, AZ"},
        
        # ========== CALIFORNIA (major expansion) ==========
        {"name": "Cathedral of the Blessed Sacrament", "diocese": "Diocese of Sacramento", "city": "Sacramento", "state": "CA", "country": "United States", "latitude": 38.5767, "longitude": -121.4934, "address": "1017 11th St, Sacramento, CA"},
        {"name": "St. Mary's Cathedral", "diocese": "Diocese of San Diego", "city": "San Diego", "state": "CA", "country": "United States", "latitude": 32.7157, "longitude": -117.1611, "address": "1546 State St, San Diego, CA"},
        {"name": "Christ Cathedral", "diocese": "Diocese of Orange", "city": "Garden Grove", "state": "CA", "country": "United States", "latitude": 33.7747, "longitude": -117.9415, "address": "13280 Chapman Ave, Garden Grove, CA"},
        {"name": "Cathedral of Our Lady of Perpetual Help", "diocese": "Diocese of Fresno", "city": "Fresno", "state": "CA", "country": "United States", "latitude": 36.7378, "longitude": -119.7871, "address": "2814 Mariposa St, Fresno, CA"},
        
        # ========== CONNECTICUT ==========
        {"name": "Cathedral of St. Joseph", "diocese": "Archdiocese of Hartford", "city": "Hartford", "state": "CT", "country": "United States", "latitude": 41.7658, "longitude": -72.6734, "address": "140 Farmington Ave, Hartford, CT"},
        
        # ========== DELAWARE ==========
        {"name": "Cathedral of St. Peter", "diocese": "Diocese of Wilmington", "city": "Wilmington", "state": "DE", "country": "United States", "latitude": 39.7392, "longitude": -75.5469, "address": "500 N West St, Wilmington, DE"},
        
        # ========== FLORIDA (major expansion) ==========
        {"name": "St. Jude Cathedral", "diocese": "Diocese of St. Petersburg", "city": "St. Petersburg", "state": "FL", "country": "United States", "latitude": 27.7676, "longitude": -82.6403, "address": "5815 5th Ave N, St. Petersburg, FL"},
        {"name": "Mary, Queen of the Universe Shrine", "diocese": "Diocese of Orlando", "city": "Orlando", "state": "FL", "country": "United States", "latitude": 28.4704, "longitude": -81.4346, "address": "8300 Vineland Ave, Orlando, FL"},
        {"name": "St. Mary Cathedral", "diocese": "Diocese of St. Augustine", "city": "St. Augustine", "state": "FL", "country": "United States", "latitude": 29.8970, "longitude": -81.3124, "address": "256 Cathedral Pl, St. Augustine, FL"},
        
        # ========== GEORGIA ==========
        {"name": "Cathedral of St. John the Baptist", "diocese": "Diocese of Savannah", "city": "Savannah", "state": "GA", "country": "United States", "latitude": 32.0744, "longitude": -81.0954, "address": "222 E Harris St, Savannah, GA"},
        
        # ========== HAWAII ==========
        {"name": "Cathedral Basilica of Our Lady of Peace", "diocese": "Diocese of Honolulu", "city": "Honolulu", "state": "HI", "country": "United States", "latitude": 21.3099, "longitude": -157.8581, "address": "1184 Bishop St, Honolulu, HI"},
        
        # ========== IDAHO ==========
        {"name": "Cathedral of St. John the Evangelist", "diocese": "Diocese of Boise", "city": "Boise", "state": "ID", "country": "United States", "latitude": 43.6150, "longitude": -116.2023, "address": "807 N 8th St, Boise, ID"},
        
        # ========== ILLINOIS (expand Chicago) ==========
        {"name": "St. Peter Catholic Church", "diocese": "Archdiocese of Chicago", "city": "Chicago", "state": "IL", "country": "United States", "latitude": 41.8967, "longitude": -87.6394, "address": "110 W Madison St, Chicago, IL"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Springfield", "city": "Springfield", "state": "IL", "country": "United States", "latitude": 39.8014, "longitude": -89.6445, "address": "524 E Lawrence Ave, Springfield, IL"},
        
        # ========== INDIANA ==========
        {"name": "Cathedral of Saints Peter and Paul", "diocese": "Archdiocese of Indianapolis", "city": "Indianapolis", "state": "IN", "country": "United States", "latitude": 39.7684, "longitude": -86.1581, "address": "1347 N Meridian St, Indianapolis, IN"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Fort Wayne-South Bend", "city": "Fort Wayne", "state": "IN", "country": "United States", "latitude": 41.0793, "longitude": -85.1394, "address": "1122 S Clinton St, Fort Wayne, IN"},
        
        # ========== IOWA ==========
        {"name": "Cathedral of St. Raphael", "diocese": "Archdiocese of Dubuque", "city": "Dubuque", "state": "IA", "country": "United States", "latitude": 42.5006, "longitude": -90.6648, "address": "231 Bluff St, Dubuque, IA"},
        {"name": "Cathedral Church of St. Ambrose", "diocese": "Diocese of Des Moines", "city": "Des Moines", "state": "IA", "country": "United States", "latitude": 41.5868, "longitude": -93.6250, "address": "607 High St, Des Moines, IA"},
        
        # ========== KANSAS ==========
        {"name": "Cathedral of St. Peter", "diocese": "Archdiocese of Kansas City", "city": "Kansas City", "state": "KS", "country": "United States", "latitude": 39.1141, "longitude": -94.5853, "address": "409 N 15th St, Kansas City, KS"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Wichita", "city": "Wichita", "state": "KS", "country": "United States", "latitude": 37.6872, "longitude": -97.3301, "address": "307 E Central Ave, Wichita, KS"},
        
        # ========== LOUISIANA ==========
        {"name": "St. Joseph Cathedral", "diocese": "Diocese of Baton Rouge", "city": "Baton Rouge", "state": "LA", "country": "United States", "latitude": 30.4515, "longitude": -91.1871, "address": "412 N St, Baton Rouge, LA"},
        {"name": "Cathedral of St. John the Evangelist", "diocese": "Diocese of Lafayette", "city": "Lafayette", "state": "LA", "country": "United States", "latitude": 30.2241, "longitude": -92.0198, "address": "914 St John St, Lafayette, LA"},
        
        # ========== MAINE ==========
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Portland", "city": "Portland", "state": "ME", "country": "United States", "latitude": 43.6615, "longitude": -70.2553, "address": "307 Congress St, Portland, ME"},
        
        # ========== MARYLAND ==========
        {"name": "Basilica of the National Shrine", "diocese": "Archdiocese of Baltimore", "city": "Baltimore", "state": "MD", "country": "United States", "latitude": 39.2962, "longitude": -76.6155, "address": "409 W Mulberry St, Baltimore, MD"},
        
        # ========== MICHIGAN ==========
        {"name": "Cathedral of the Most Blessed Sacrament", "diocese": "Archdiocese of Detroit", "city": "Detroit", "state": "MI", "country": "United States", "latitude": 42.3587, "longitude": -83.0632, "address": "9844 Woodward Ave, Detroit, MI"},
        {"name": "St. Andrew Cathedral", "diocese": "Diocese of Grand Rapids", "city": "Grand Rapids", "state": "MI", "country": "United States", "latitude": 42.9634, "longitude": -85.6681, "address": "215 Sheldon Ave SE, Grand Rapids, MI"},
        
        # ========== MINNESOTA ==========
        {"name": "Cathedral of St. Paul", "diocese": "Archdiocese of Saint Paul and Minneapolis", "city": "St. Paul", "state": "MN", "country": "United States", "latitude": 44.9463, "longitude": -93.1041, "address": "239 Selby Ave, St. Paul, MN"},
        {"name": "Basilica of St. Mary", "diocese": "Archdiocese of Saint Paul and Minneapolis", "city": "Minneapolis", "state": "MN", "country": "United States", "latitude": 44.9736, "longitude": -93.2826, "address": "1600 Hennepin Ave, Minneapolis, MN"},
        
        # ========== MISSISSIPPI ==========
        {"name": "Cathedral of St. Peter the Apostle", "diocese": "Diocese of Jackson", "city": "Jackson", "state": "MS", "country": "United States", "latitude": 32.2988, "longitude": -90.1848, "address": "123 N West St, Jackson, MS"},
        
        # ========== MISSOURI ==========
        {"name": "Cathedral Basilica of St. Louis", "diocese": "Archdiocese of St. Louis", "city": "St. Louis", "state": "MO", "country": "United States", "latitude": 38.6517, "longitude": -90.2590, "address": "4431 Lindell Blvd, St. Louis, MO"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Kansas City-St. Joseph", "city": "Kansas City", "state": "MO", "country": "United States", "latitude": 39.1002, "longitude": -94.5786, "address": "416 W 12th St, Kansas City, MO"},
        
        # ========== MONTANA ==========
        {"name": "Cathedral of St. Helena", "diocese": "Diocese of Helena", "city": "Helena", "state": "MT", "country": "United States", "latitude": 46.5972, "longitude": -112.0203, "address": "530 N Ewing St, Helena, MT"},
        
        # ========== NEBRASKA ==========
        {"name": "St. Cecilia Cathedral", "diocese": "Archdiocese of Omaha", "city": "Omaha", "state": "NE", "country": "United States", "latitude": 41.2587, "longitude": -95.9378, "address": "701 N 40th St, Omaha, NE"},
        
        # ========== NEW HAMPSHIRE ==========
        {"name": "St. Joseph Cathedral", "diocese": "Diocese of Manchester", "city": "Manchester", "state": "NH", "country": "United States", "latitude": 42.9956, "longitude": -71.4548, "address": "145 Lowell St, Manchester, NH"},
        
        # ========== NEW JERSEY ==========
        {"name": "Cathedral Basilica of the Sacred Heart", "diocese": "Archdiocese of Newark", "city": "Newark", "state": "NJ", "country": "United States", "latitude": 40.7445, "longitude": -74.1747, "address": "89 Ridge St, Newark, NJ"},
        {"name": "Cathedral of St. John the Baptist", "diocese": "Diocese of Paterson", "city": "Paterson", "state": "NJ", "country": "United States", "latitude": 40.9168, "longitude": -74.1718, "address": "381 Grand St, Paterson, NJ"},
        
        # ========== NEW MEXICO ==========
        {"name": "Cathedral Basilica of St. Francis of Assisi", "diocese": "Archdiocese of Santa Fe", "city": "Santa Fe", "state": "NM", "country": "United States", "latitude": 35.6870, "longitude": -105.9378, "address": "131 Cathedral Pl, Santa Fe, NM"},
        
        # ========== NEW YORK (major expansion) ==========
        {"name": "St. Joseph's Cathedral", "diocese": "Diocese of Buffalo", "city": "Buffalo", "state": "NY", "country": "United States", "latitude": 42.8864, "longitude": -78.8784, "address": "50 Franklin St, Buffalo, NY"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Albany", "city": "Albany", "state": "NY", "country": "United States", "latitude": 42.6526, "longitude": -73.7562, "address": "125 Eagle St, Albany, NY"},
        {"name": "Cathedral of the Sacred Heart", "diocese": "Diocese of Rochester", "city": "Rochester", "state": "NY", "country": "United States", "latitude": 43.1566, "longitude": -77.6088, "address": "296 Flower City Park, Rochester, NY"},
        
        # ========== NORTH CAROLINA ==========
        {"name": "Sacred Heart Cathedral", "diocese": "Diocese of Raleigh", "city": "Raleigh", "state": "NC", "country": "United States", "latitude": 35.7796, "longitude": -78.6382, "address": "200 Hillsborough St, Raleigh, NC"},
        
        # ========== NORTH DAKOTA ==========
        {"name": "Cathedral of the Holy Spirit", "diocese": "Diocese of Bismarck", "city": "Bismarck", "state": "ND", "country": "United States", "latitude": 46.8083, "longitude": -100.7837, "address": "520 N Raymond St, Bismarck, ND"},
        
        # ========== OHIO ==========
        {"name": "Cathedral of St. Peter in Chains", "diocese": "Archdiocese of Cincinnati", "city": "Cincinnati", "state": "OH", "country": "United States", "latitude": 39.1031, "longitude": -84.5120, "address": "325 W 8th St, Cincinnati, OH"},
        {"name": "Cathedral of St. John the Evangelist", "diocese": "Diocese of Cleveland", "city": "Cleveland", "state": "OH", "country": "United States", "latitude": 41.4993, "longitude": -81.6944, "address": "1007 Superior Ave E, Cleveland, OH"},
        {"name": "St. Joseph Cathedral", "diocese": "Diocese of Columbus", "city": "Columbus", "state": "OH", "country": "United States", "latitude": 39.9612, "longitude": -82.9988, "address": "212 E Broad St, Columbus, OH"},
        
        # ========== OKLAHOMA ==========
        {"name": "Cathedral of Our Lady of Perpetual Help", "diocese": "Archdiocese of Oklahoma City", "city": "Oklahoma City", "state": "OK", "country": "United States", "latitude": 35.4676, "longitude": -97.5164, "address": "3214 N Lake Ave, Oklahoma City, OK"},
        
        # ========== OREGON ==========
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Archdiocese of Portland", "city": "Portland", "state": "OR", "country": "United States", "latitude": 45.5234, "longitude": -122.6762, "address": "1716 NW Davis St, Portland, OR"},
        
        # ========== PENNSYLVANIA ==========
        {"name": "St. Paul Cathedral", "diocese": "Diocese of Pittsburgh", "city": "Pittsburgh", "state": "PA", "country": "United States", "latitude": 40.4406, "longitude": -79.9959, "address": "108 N Dithridge St, Pittsburgh, PA"},
        {"name": "Cathedral of St. Patrick", "diocese": "Diocese of Harrisburg", "city": "Harrisburg", "state": "PA", "country": "United States", "latitude": 40.2732, "longitude": -76.8867, "address": "212 State St, Harrisburg, PA"},
        
        # ========== RHODE ISLAND ==========
        {"name": "Cathedral of Saints Peter and Paul", "diocese": "Diocese of Providence", "city": "Providence", "state": "RI", "country": "United States", "latitude": 41.8240, "longitude": -71.4128, "address": "30 Fenner St, Providence, RI"},
        
        # ========== SOUTH CAROLINA ==========
        {"name": "Cathedral of St. John the Baptist", "diocese": "Diocese of Charleston", "city": "Charleston", "state": "SC", "country": "United States", "latitude": 32.7765, "longitude": -79.9311, "address": "120 Broad St, Charleston, SC"},
        
        # ========== SOUTH DAKOTA ==========
        {"name": "Cathedral of St. Joseph", "diocese": "Diocese of Sioux Falls", "city": "Sioux Falls", "state": "SD", "country": "United States", "latitude": 43.5446, "longitude": -96.7311, "address": "521 N Duluth Ave, Sioux Falls, SD"},
        
        # ========== TENNESSEE ==========
        {"name": "Cathedral of the Most Sacred Heart of Jesus", "diocese": "Diocese of Knoxville", "city": "Knoxville", "state": "TN", "country": "United States", "latitude": 35.9606, "longitude": -83.9207, "address": "711 S Northshore Dr, Knoxville, TN"},
        {"name": "Cathedral of the Immaculate Conception", "diocese": "Diocese of Memphis", "city": "Memphis", "state": "TN", "country": "United States", "latitude": 35.1495, "longitude": -90.0490, "address": "1695 Central Ave, Memphis, TN"},
        
        # ========== TEXAS (major expansion) ==========
        {"name": "Co-Cathedral of the Sacred Heart", "diocese": "Diocese of Dallas", "city": "Dallas", "state": "TX", "country": "United States", "latitude": 32.7767, "longitude": -96.7970, "address": "1511 Ross Ave, Dallas, TX"},
        {"name": "St. Mary's Cathedral", "diocese": "Diocese of Austin", "city": "Austin", "state": "TX", "country": "United States", "latitude": 30.2672, "longitude": -97.7431, "address": "203 E 10th St, Austin, TX"},
        {"name": "St. Mary Cathedral Basilica", "diocese": "Archdiocese of Galveston-Houston", "city": "Galveston", "state": "TX", "country": "United States", "latitude": 29.3013, "longitude": -94.7977, "address": "2011 Church St, Galveston, TX"},
        {"name": "Cathedral of the Sacred Heart", "diocese": "Diocese of El Paso", "city": "El Paso", "state": "TX", "country": "United States", "latitude": 31.7619, "longitude": -106.4850, "address": "602 N Oregon St, El Paso, TX"},
        
        # ========== UTAH ==========
        {"name": "Cathedral of the Madeleine", "diocese": "Diocese of Salt Lake City", "city": "Salt Lake City", "state": "UT", "country": "United States", "latitude": 40.7740, "longitude": -111.8910, "address": "331 E South Temple, Salt Lake City, UT"},
        
        # ========== VERMONT ==========
        {"name": "Cathedral of St. Joseph", "diocese": "Diocese of Burlington", "city": "Burlington", "state": "VT", "country": "United States", "latitude": 44.4759, "longitude": -73.2121, "address": "85 Elmwood Ave, Burlington, VT"},
        
        # ========== VIRGINIA ==========
        {"name": "Cathedral of the Sacred Heart", "diocese": "Diocese of Richmond", "city": "Richmond", "state": "VA", "country": "United States", "latitude": 37.5407, "longitude": -77.4360, "address": "823 Cathedral Pl, Richmond, VA"},
        {"name": "Cathedral of St. Thomas More", "diocese": "Diocese of Arlington", "city": "Arlington", "state": "VA", "country": "United States", "latitude": 38.8816, "longitude": -77.1945, "address": "3901 Cathedral Ln, Arlington, VA"},
        
        # ========== WASHINGTON (add more) ==========
        {"name": "St. Joseph Cathedral", "diocese": "Diocese of Spokane", "city": "Spokane", "state": "WA", "country": "United States", "latitude": 47.6588, "longitude": -117.4260, "address": "505 S Stone St, Spokane, WA"},
        
        # ========== WEST VIRGINIA ==========
        {"name": "Cathedral of St. Joseph", "diocese": "Diocese of Wheeling-Charleston", "city": "Wheeling", "state": "WV", "country": "United States", "latitude": 40.0640, "longitude": -80.7209, "address": "1218 Eoff St, Wheeling, WV"},
        
        # ========== WISCONSIN ==========
        {"name": "Cathedral of St. John the Evangelist", "diocese": "Archdiocese of Milwaukee", "city": "Milwaukee", "state": "WI", "country": "United States", "latitude": 43.0389, "longitude": -87.9065, "address": "812 N Jackson St, Milwaukee, WI"},
        {"name": "St. Joseph Cathedral", "diocese": "Diocese of La Crosse", "city": "La Crosse", "state": "WI", "country": "United States", "latitude": 43.8136, "longitude": -91.2393, "address": "530 Main St, La Crosse, WI"},
        
        # ========== WYOMING ==========
        {"name": "St. Matthew's Cathedral", "diocese": "Diocese of Cheyenne", "city": "Cheyenne", "state": "WY", "country": "United States", "latitude": 41.1400, "longitude": -104.8202, "address": "2107 Capitol Ave, Cheyenne, WY"},
    ]
    
    print(f"📊 Total parishes to add: {len(parishes)}\n")
    
    with ParishDatabase("parishes.db") as db:
        added = 0
        skipped = 0
        states = set()
        
        for parish in parishes:
            states.add(parish['state'])
            if not db.parish_exists(parish['name'], parish.get('diocese', 'Unknown')):
                parish_id = db.insert_parish(parish)
                added += 1
                print(f"  ✓ {parish['state']}: {parish['name']} - {parish['city']}")
            else:
                skipped += 1
        
        stats = db.get_stats()
        print("\n" + "="*70)
        print("📊 PHASE 1 COMPLETE - USA EXPANSION")
        print("="*70)
        print(f"  Total parishes in database: {stats['total_parishes']}")
        print(f"  USA states covered: {len(states)} states")
        print(f"  Added in this phase: {added} parishes")
        print(f"  Skipped (already exist): {skipped} parishes")
        print(f"\n✅ Phase 1 Complete! Ready for Phase 2 (Philippines)")

if __name__ == '__main__':
    main()
