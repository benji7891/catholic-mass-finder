"""Geocoding service to convert addresses to coordinates."""
import time
from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class Geocoder:
    """Handles geocoding of addresses to latitude/longitude."""
    
    def __init__(self):
        """Initialize geocoder with Nominatim (OpenStreetMap)."""
        self.geolocator = Nominatim(user_agent="CatholicMassFinderBot/1.0")
        self.cache = {}  # Simple in-memory cache
        
    def geocode(self, address: str, city: str = None, state: str = None, 
                zip_code: str = None, max_retries: int = 3) -> Optional[Tuple[float, float]]:
        """
        Convert address to coordinates.
        
        Args:
            address: Street address
            city: City name
            state: State abbreviation
            zip_code: ZIP code
            max_retries: Maximum retry attempts
            
        Returns:
            Tuple of (latitude, longitude) or None if geocoding fails
        """
        # Build full address
        address_parts = [address]
        if city:
            address_parts.append(city)
        if state:
            address_parts.append(state)
        if zip_code:
            address_parts.append(zip_code)
        
        full_address = ", ".join(filter(None, address_parts))
        
        # Check cache
        if full_address in self.cache:
            return self.cache[full_address]
        
        # Try geocoding with retries
        for attempt in range(max_retries):
            try:
                location = self.geolocator.geocode(full_address)
                
                if location:
                    coords = (location.latitude, location.longitude)
                    self.cache[full_address] = coords
                    
                    # Validate coordinates are in expected state if provided
                    if state and not self._validate_state(location.address, state):
                        print(f"⚠️  Warning: Geocoded to wrong state: {full_address}")
                    
                    # Rate limit: 1 request per second for Nominatim
                    time.sleep(1)
                    return coords
                else:
                    print(f"❌ Geocoding failed: {full_address}")
                    return None
                    
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                if attempt < max_retries - 1:
                    print(f"⚠️  Geocoding timeout, retrying... ({attempt + 1}/{max_retries})")
                    time.sleep(2)
                else:
                    print(f"❌ Geocoding error after {max_retries} attempts: {full_address}")
                    return None
                    
        return None
        
    def _validate_state(self, geocoded_address: str, expected_state: str) -> bool:
        """Validate that geocoded address is in expected state."""
        # Simple check - look for state abbreviation in geocoded address
        return expected_state.upper() in geocoded_address.upper()
        
    def geocode_batch(self, addresses: list, delay: float = 1.0) -> dict:
        """
        Geocode multiple addresses with rate limiting.
        
        Args:
            addresses: List of address dictionaries
            delay: Delay between requests in seconds
            
        Returns:
            Dictionary mapping address to coordinates
        """
        results = {}
        
        for addr_dict in addresses:
            full_addr = addr_dict.get('full_address', '')
            coords = self.geocode(
                addr_dict.get('address', ''),
                addr_dict.get('city'),
                addr_dict.get('state'),
                addr_dict.get('zip')
            )
            results[full_addr] = coords
            time.sleep(delay)
            
        return results
