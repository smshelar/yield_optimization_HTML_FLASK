from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly
import json


from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app)

# Load Dataset

df = pd.read_csv('data/manufacturing_data.csv')

@app.route('/')
def dashboard():
    avg_yield = round(df['yield_percentage'].mean(), 2)


    gauge_chart = go.Figure(go.Indicator(
        mode='gauge+number',
        value=avg_yield,
        title={'text': 'Yield Efficiency'},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': '#00D9FF'},
            'steps': [
                {'range': [0, 70], 'color': '#ff4d4d'},
                {'range': [70, 85], 'color': '#ffaa00'},
                {'range': [85, 100], 'color': '#00ff99'}
            ]
        }
    ))

    gauge_chart.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1C2541',
    plot_bgcolor='#1C2541',
    font_color='white'
    )

    avg_scrap = round(df['scrap_rate'].mean(), 2)
    avg_quality = round(df['quality_score'].mean(), 2)
    avg_energy = round(df['energy_consumption'].mean(), 2)

    # Yield Trend
    trend_df = (
        df.groupby('timestamp')['yield_percentage']
        .mean()
        .reset_index()
    )

    line_chart = px.line(
        trend_df,
        x='timestamp',
        y='yield_percentage',
        title='Yield Trend Over Time'
    )

    line_chart.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1C2541',
    plot_bgcolor='#1C2541',
    font_color='white'
    )

    line_graphJSON = json.dumps(
        line_chart,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    # Plant Benchmarking
    benchmark_df = (
        df.groupby('plant_id')[
            ['yield_percentage', 'scrap_rate']
        ]
        .mean()
        .reset_index()
    )

    bar_chart = px.bar(
        benchmark_df,
        x='plant_id',
        y='yield_percentage',
        color='scrap_rate',
        title='Cross Plant Benchmarking'
    )

    bar_chart.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1C2541',
    plot_bgcolor='#1C2541',
    font_color='white'
    )

    bar_graphJSON = json.dumps(
        bar_chart,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    gauge_graphJSON = json.dumps(
    gauge_chart,
    cls=plotly.utils.PlotlyJSONEncoder
    )

    return render_template(
    'dashboard.html',
    avg_yield=avg_yield,
    avg_scrap=avg_scrap,
    avg_quality=avg_quality,
    avg_energy=avg_energy,
    line_graphJSON=line_graphJSON,
    bar_graphJSON=bar_graphJSON,
    gauge_graphJSON=gauge_graphJSON
    )


@app.route('/monitoring')
def monitoring():

    sensor_df = df.tail(300)

    sensor_chart = px.line(
        sensor_df,
        x='timestamp',
        y=['temperature', 'pressure', 'humidity'],
        title='Process Sensor Monitoring'
    )

    sensor_graphJSON = json.dumps(
        sensor_chart,
        cls=plotly.utils.PlotlyJSONEncoder
    )

    return render_template(
        'monitoring.html',
        sensor_graphJSON=sensor_graphJSON
    )

@app.route('/benchmarking')
def benchmarking():

    benchmark_df = (
        df.groupby('plant_id')[
            [
                'yield_percentage',
                'scrap_rate',
                'quality_score',
                'energy_consumption'
            ]
        ]
        .mean()
        .reset_index()
    )

    return render_template(
        'benchmarking.html',
        tables=[benchmark_df.to_html(classes='table table-dark table-striped')]
    )

@app.route('/recommendations')
def recommendations():

    latest = df.tail(12).to_dict(orient='records')

    recommendations_data = []

    for row in latest:

        recommendation = []

        if row['humidity'] > 60:
            recommendation.append('Reduce humidity below 55%')

        if row['vibration'] > 5:
            recommendation.append('Inspect machine vibration levels')

        if row['temperature'] < 175:
            recommendation.append('Increase process temperature by 3°C')

        if len(recommendation) == 0:
            recommendation.append('Process operating optimally')

        row['recommendations'] = recommendation

        recommendations_data.append(row)

    return render_template(
        'recommendations.html',
        data=recommendations_data
    )

@app.route('/semantic-layer')
def semantic_layer():

    semantic_kpis = [
        {
            'name': 'Yield Percentage',
            'definition': 'Good Units / Total Units',
            'owner': 'Manufacturing',
            'source': 'Historian'
        },
        {
            'name': 'Scrap Rate',
            'definition': 'Scrap Units / Total Production',
            'owner': 'Production',
            'source': 'MES'
        },
        {
            'name': 'Quality Score',
            'definition': 'Weighted Quality Metric',
            'owner': 'Quality Team',
            'source': 'LIMS'
        },
        {
            'name': 'Energy Consumption',
            'definition': 'Energy Usage Per Batch',
            'owner': 'Operations',
            'source': 'IoT Sensors'
        }
    ]

    return render_template(
        'semantic_layer.html',
        kpis=semantic_kpis
    )

    @socketio.on('connect')
    def connect():
        print('Client connected')

    corr = df[
    [
        'temperature',
        'pressure',
        'humidity',
        'machine_speed',
        'vibration',
        'yield_percentage',
        'scrap_rate'
    ]
    ].corr()


    heatmap = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='Blues',
    title='Process Correlation Heatmap'
    )

    heatmap.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1C2541',
        plot_bgcolor='#1C2541',
        font_color='white'
    )

    heatmapJSON = json.dumps(
    heatmap,
    cls=plotly.utils.PlotlyJSONEncoder
    )

    heatmapJSON=heatmapJSON

if __name__ == '__main__':
    socketio.run(app, debug=True)