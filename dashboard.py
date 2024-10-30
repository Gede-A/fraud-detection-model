import dash
from dash import dcc, html, Input, Output
import requests
import plotly.express as px

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Fraud Detection Insights"),

    # Interval component for periodic updates
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Updates every minute (60000 milliseconds)
        n_intervals=0
    ),

    # Summary statistics
    html.Div(id='summary'),

    # Fraud trend over time
    dcc.Graph(id='fraud-trend'),

    # Fraud by geography
    dcc.Graph(id='fraud-geo'),

    # Fraud by device/browser
    dcc.Graph(id='fraud-device-browser')
])

# Callback to update summary statistics
@app.callback(Output('summary', 'children'), Input('interval-component', 'n_intervals'))
def update_summary(n):
    try:
        summary = requests.get('http://127.0.0.1:5000/summary').json()
        return html.Div([
            html.P(f"Total Transactions: {summary.get('total_transactions', 'N/A')}"),
            html.P(f"Fraud Cases: {summary.get('fraud_cases', 'N/A')}"),
            html.P(f"Fraud Percentage: {summary.get('fraud_percentage', 'N/A')}%")
        ])
    except Exception as e:
        return html.Div(f"Error fetching summary data: {e}")

# Callback to update fraud trend line chart
@app.callback(Output('fraud-trend', 'figure'), Input('interval-component', 'n_intervals'))
def update_trend(n):
    try:
        trend = requests.get('http://127.0.0.1:5000/fraud_trend').json()
        fig = px.line(trend, x='Date', y='Fraud', title='Fraud Cases Over Time')
        return fig
    except Exception as e:
        return px.line(title=f"Error fetching trend data: {e}")

# Callback for geographic fraud
@app.callback(Output('fraud-geo', 'figure'), Input('interval-component', 'n_intervals'))
def update_geo(n):
    try:
        geo_data = requests.get('http://127.0.0.1:5000/fraud_by_geo').json()
        fig = px.choropleth(geo_data, locations='Country', color='Fraud', title='Fraud Cases by Country')
        return fig
    except Exception as e:
        return px.choropleth(title=f"Error fetching geo data: {e}")

# Callback for device/browser chart
@app.callback(Output('fraud-device-browser', 'figure'), Input('interval-component', 'n_intervals'))
def update_device_browser(n):
    try:
        device_data = requests.get('http://127.0.0.1:5000/fraud_by_device').json()
        fig = px.bar(device_data, x='Device', y='Fraud', color='Browser', barmode='group', title='Fraud Cases by Device and Browser')
        return fig
    except Exception as e:
        return px.bar(title=f"Error fetching device/browser data: {e}")

if __name__ == '__main__':
    app.run_server(debug=True)
