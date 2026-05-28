import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

NUM_RECORDS = 5000

plants = ["Plant_A", "Plant_B", "Plant_C"]
lines = ["Line_1", "Line_2", "Line_3"]
shifts = ["Morning", "Evening", "Night"]

records = []

start_date = datetime.now() - timedelta(days=90)

for i in range(NUM_RECORDS):

    timestamp = start_date + timedelta(minutes=i * 30)

    plant = random.choice(plants)
    line = random.choice(lines)
    shift = random.choice(shifts)

    temperature = round(np.random.normal(180, 8), 2)
    pressure = round(np.random.normal(35, 3), 2)
    humidity = round(np.random.normal(55, 10), 2)
    machine_speed = round(np.random.normal(120, 15), 2)
    vibration = round(np.random.normal(4, 1.2), 2)
    raw_material_quality = round(np.random.uniform(70, 100), 2)
    energy_consumption = round(np.random.normal(450, 40), 2)
    downtime_minutes = max(0, round(np.random.normal(12, 5), 2))

    noise = np.random.normal(0, 2)

    yield_percentage = (
        82
        + (raw_material_quality * 0.12)
        - (humidity * 0.08)
        + (temperature * 0.03)
        - (vibration * 1.5)
        - (downtime_minutes * 0.2)
        + noise
    )

    yield_percentage = round(max(65, min(yield_percentage, 99)), 2)

    scrap_rate = round(100 - yield_percentage + np.random.uniform(0, 3), 2)

    quality_score = round(
        (yield_percentage * 0.7)
        + (raw_material_quality * 0.3),
        2
    )

    predicted_yield = round(
        yield_percentage + np.random.normal(0, 1),
        2
    )

    recommended_temperature = round(temperature + np.random.uniform(-3, 3), 2)
    recommended_pressure = round(pressure + np.random.uniform(-2, 2), 2)

    adoption_flag = random.choice([0, 1])

    records.append({
        "timestamp": timestamp,
        "plant_id": plant,
        "production_line": line,
        "batch_id": fake.uuid4(),
        "temperature": temperature,
        "pressure": pressure,
        "humidity": humidity,
        "machine_speed": machine_speed,
        "vibration": vibration,
        "raw_material_quality": raw_material_quality,
        "energy_consumption": energy_consumption,
        "operator_shift": shift,
        "yield_percentage": yield_percentage,
        "scrap_rate": scrap_rate,
        "quality_score": quality_score,
        "downtime_minutes": downtime_minutes,
        "recommended_temperature": recommended_temperature,
        "recommended_pressure": recommended_pressure,
        "adoption_flag": adoption_flag,
        "predicted_yield": predicted_yield
    })


df = pd.DataFrame(records)

output_path = "data/manufacturing_data.csv"

df.to_csv(output_path, index=False)

print("Dataset generated successfully")
print(df.head())