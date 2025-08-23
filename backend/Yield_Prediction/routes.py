# api.py

import os
import pickle
import numpy as np
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
from huggingface_hub import hf_hub_download
from fastapi.middleware.cors import CORSMiddleware

# --- 1. Initialize FastAPI app ---
router = APIRouter()

# --- 2. Load The Trained Models ---

# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
recommend_model_path = hf_hub_download(
    repo_id="adityaarun1010/my-new-models",
    filename="crop_recommend_model.pkl"
)


yield_model_path = hf_hub_download(
    repo_id="adityaarun1010/my-new-models",
    filename="crop_yield_model.pkl"
)


try:
    with open(recommend_model_path, 'rb') as file:
        recommend_model = pickle.load(file)
    print("✅ Crop recommendation model loaded successfully.")
except FileNotFoundError:
    print(f"❌ Error: Recommendation model not found at {recommend_model_path}")
    recommend_model = None

try:
    with open(yield_model_path, 'rb') as file:
        yield_model_pipeline = pickle.load(file)
    print("✅ Crop yield prediction model loaded successfully.")
except FileNotFoundError:
    print(f"❌ Error: Yield model not found at {yield_model_path}")
    yield_model_pipeline = None

# --- 3. Define the Input Data Model using Pydantic ---
# This ensures that the data sent from the frontend matches what the model expects.
class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float
    State_Name: str
    District_Name: str
    Season: str
    Crop_Year: int = 2024 # Default to current year or make it an input

# --- 4. Create the Prediction Endpoint ---
@router.post("/predict-yield")
async def predict_yield(data: CropInput):
    if not recommend_model or not yield_model_pipeline:
        return {"error": "Models are not loaded. Please check server logs."}

    try:
        # Part A: Predict Crop Recommendation
        recommend_features_df = pd.DataFrame(
            [[data.N, data.P, data.K, data.temperature, data.humidity, data.ph, data.rainfall]],
            columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        )
        recommended_crop = recommend_model.predict(recommend_features_df)[0]

        # Part B: Predict Yield for the Recommended Crop
        yield_features_df = pd.DataFrame({
            'State_Name': [data.State_Name],
            'District_Name': [data.District_Name],
            'Crop_Year': [data.Crop_Year],
            'Season': [data.Season],
            'Crop': [recommended_crop]
        })
        
        predicted_log_yield = yield_model_pipeline.predict(yield_features_df)
        # Extract the float value from the numpy array
        predicted_yield = np.expm1(predicted_log_yield)

        # Return the results as JSON
        return {
            "recommended_crop": recommended_crop.upper(),
            "predicted_yield": f"{predicted_yield[0]:.2f}"
        }
    except Exception as e:
        return {"error": f"An error occurred during prediction: {str(e)}"}

# --- 5. Root endpoint for testing ---
@router.get("/")
def read_root():
    return {"message": "LeafLense Yield Prediction API is running."}

