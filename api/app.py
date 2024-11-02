from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
fraud_data = pd.read_csv('../data/fraud_data.csv')

# Check column names to ensure they match
if 'purchase_time' not in fraud_data.columns:
    fraud_data.rename(columns={'purchase_time': 'purchase_time'}, inplace=True)

# Endpoint for summary statistics
@app.route('/summary', methods=['GET'])
def summary():
    total_transactions = fraud_data.shape[0]
    fraud_cases = fraud_data[fraud_data['class'] == 1].shape[0]
    fraud_percentage = (fraud_cases / total_transactions) * 100
    return jsonify({
        "total_transactions": total_transactions,
        "fraud_cases": fraud_cases,
        "fraud_percentage": fraud_percentage
    })

# Endpoint for fraud trend over time
@app.route('/fraud_trend', methods=['GET'])
def fraud_trend():
    trend_data = fraud_data.groupby('purchase_time')['class'].sum().reset_index()
    trend_data.columns = ['Date', 'Fraud']  # Ensure column names match those used in Dash
    return jsonify(trend_data.to_dict(orient='records'))

# Endpoint for geographic fraud distribution
@app.route('/fraud_by_geo', methods=['GET'])
def fraud_by_geo():
    geo_data = fraud_data.groupby('country')['class'].sum().reset_index()
    geo_data.columns = ['country', 'Fraud']  # Ensure column names match those used in Dash
    return jsonify(geo_data.to_dict(orient='records'))

# Endpoint for device/browser fraud distribution
@app.route('/fraud_by_device', methods=['GET'])
def fraud_by_device():
    device_data = fraud_data.groupby(['device_id', 'browser'])['class'].sum().reset_index()
    device_data.columns = ['Device', 'Browser', 'Fraud']  # Ensure column names match those used in Dash
    return jsonify(device_data.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(debug=True)
