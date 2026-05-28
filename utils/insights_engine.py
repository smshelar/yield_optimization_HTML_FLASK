import pandas as pd


def generate_insights(df):

    insights = []

    high_humidity = df[df['humidity'] > 60]

    if len(high_humidity) > 0:
        insights.append(
            'High humidity strongly impacts yield reduction.'
        )

    high_vibration = df[df['vibration'] > 5]

    if len(high_vibration) > 0:
        insights.append(
            'Machine vibration increases scrap probability.'
        )

    low_quality = df[df['quality_score'] < 80]

    if len(low_quality) > 0:
        insights.append(
            'Low quality batches detected in Plant B.'
        )

    return insights