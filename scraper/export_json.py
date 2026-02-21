#!/usr/bin/env python3
"""Export parishes database to JSON."""
from database import ParishDatabase
import json

db = ParishDatabase('parishes.db')
db.connect()
rows = db.cursor.execute('SELECT * FROM parishes').fetchall()
parishes = [dict(row) for row in rows]

with open('../public/parishes.json', 'w') as f:
    json.dump(parishes, f, indent=2)

db.close()
print(f'✅ Exported {len(parishes)} parishes to parishes.json')
