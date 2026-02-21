"""Database operations for parish data."""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class ParishDatabase:
    """Handles all database operations for parish data."""
    
    def __init__(self, db_path: str = "parishes.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        
    def connect(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            
    def initialize(self):
        """Initialize database schema from SQL file."""
        schema_path = Path(__file__).parent / "init_db.sql"
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        self.cursor.executescript(schema_sql)
        self.conn.commit()
        print(f"✅ Database initialized at {self.db_path}")
        
    def insert_parish(self, parish_data: Dict[str, Any]) -> int:
        """Insert a new parish record."""
        # Convert mass_times dict to JSON string if present
        if 'mass_times' in parish_data and isinstance(parish_data['mass_times'], dict):
            parish_data['mass_times'] = json.dumps(parish_data['mass_times'])
            
        columns = ', '.join(parish_data.keys())
        placeholders = ', '.join(['?' for _ in parish_data])
        
        query = f"INSERT INTO parishes ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(parish_data.values()))
        self.conn.commit()
        return self.cursor.lastrowid
        
    def parish_exists(self, name: str, diocese: str) -> bool:
        """Check if a parish already exists."""
        query = "SELECT id FROM parishes WHERE name = ? AND diocese = ?"
        result = self.cursor.execute(query, (name, diocese)).fetchone()
        return result is not None
        
    def update_parish(self, parish_id: int, parish_data: Dict[str, Any]):
        """Update an existing parish record."""
        # Convert mass_times dict to JSON string if present
        if 'mass_times' in parish_data and isinstance(parish_data['mass_times'], dict):
            parish_data['mass_times'] = json.dumps(parish_data['mass_times'])
            
        parish_data['last_scraped'] = datetime.now().isoformat()
        
        set_clause = ', '.join([f"{key} = ?" for key in parish_data.keys()])
        query = f"UPDATE parishes SET {set_clause} WHERE id = ?"
        
        values = list(parish_data.values()) + [parish_id]
        self.cursor.execute(query, values)
        self.conn.commit()
        
    def log_scrape(self, diocese: str, status: str, parishes_found: int, error_message: Optional[str] = None):
        """Log a scraping operation."""
        query = """
            INSERT INTO scrape_log (diocese, status, parishes_found, error_message)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (diocese, status, parishes_found, error_message))
        self.conn.commit()
        
    def get_parishes_by_diocese(self, diocese: str) -> List[Dict]:
        """Get all parishes for a diocese."""
        query = "SELECT * FROM parishes WHERE diocese = ?"
        results = self.cursor.execute(query, (diocese,)).fetchall()
        return [dict(row) for row in results]
        
    def get_parish_count(self) -> int:
        """Get total number of parishes in database."""
        query = "SELECT COUNT(*) as count FROM parishes"
        result = self.cursor.execute(query).fetchone()
        return result['count'] if result else 0
        
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {
            'total_parishes': self.get_parish_count(),
            'parishes_with_coords': self.cursor.execute(
                "SELECT COUNT(*) FROM parishes WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
            ).fetchone()[0],
            'dioceses_scraped': self.cursor.execute(
                "SELECT COUNT(DISTINCT diocese) FROM parishes"
            ).fetchone()[0],
            'states_covered': self.cursor.execute(
                "SELECT COUNT(DISTINCT state) FROM parishes"
            ).fetchone()[0],
        }
        return stats
