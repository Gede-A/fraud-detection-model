from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

# Load the pre-trained model
with open('notebooks/creditcard_model.pkl', 'rb') as file:
    model = joblib.load(file)

# Initialize the FastAPI app
app = FastAPI()

# Define the input schema for the prediction request
class CreditCardData(BaseModel):
    features: list

# Root endpoint to verify API is working
@app.get("/")
def read_root():
    return {"message": "Welcome to the Credit Card Fraud Detection API"}

# Prediction endpoint
@app.post("/predict/")
def predict(data: CreditCardData):
    # Convert input list to numpy array
    input_data = np.array(data.features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(input_data)
    
    # Return the prediction as a response
    return {"prediction": int(prediction[0])}
