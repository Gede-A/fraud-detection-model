from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
fraud_data = pd.read_csv('fraud_data.csv')

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
    return trend_data.to_dict(orient='records')

# Endpoint for geographic fraud distribution
@app.route('/fraud_by_geo', methods=['GET'])
def fraud_by_geo():
    geo_data = fraud_data.groupby('country')['class'].sum().reset_index()
    return geo_data.to_dict(orient='records')

# Endpoint for device/browser fraud distribution
@app.route('/fraud_by_device', methods=['GET'])
def fraud_by_device():
    device_data = fraud_data.groupby(['device_id', 'browser'])['class'].sum().reset_index()
    return device_data.to_dict(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
