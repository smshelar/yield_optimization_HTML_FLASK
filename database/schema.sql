CREATE TABLE manufacturing_data (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    plant_id TEXT,
    production_line TEXT,
    temperature FLOAT,
    pressure FLOAT,
    humidity FLOAT,
    machine_speed FLOAT,
    vibration FLOAT,
    yield_percentage FLOAT,
    scrap_rate FLOAT,
    quality_score FLOAT
);