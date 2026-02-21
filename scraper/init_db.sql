-- Catholic Mass Finder Parish Database Schema

CREATE TABLE IF NOT EXISTS parishes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  diocese TEXT NOT NULL,
  address TEXT,
  street TEXT,
  city TEXT,
  state TEXT,
  zip TEXT,
  country TEXT DEFAULT 'United States',
  phone TEXT,
  website TEXT,
  email TEXT,
  latitude REAL,
  longitude REAL,
  mass_times TEXT,  -- Store as JSON string
  pastor TEXT,
  source_url TEXT,  -- Original diocese page URL
  last_scraped TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_location ON parishes(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_state ON parishes(state);
CREATE INDEX IF NOT EXISTS idx_diocese ON parishes(diocese);
CREATE INDEX IF NOT EXISTS idx_city ON parishes(city);

CREATE TABLE IF NOT EXISTS scrape_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  diocese TEXT,
  status TEXT,  -- success, failed, partial
  parishes_found INTEGER,
  error_message TEXT,
  scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
