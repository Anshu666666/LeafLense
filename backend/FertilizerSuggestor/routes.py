from fastapi import APIRouter
from pydantic import BaseModel
import joblib
import pandas as pd
import json
import google.generativeai as genai
from huggingface_hub import hf_hub_download
import re
import os

router = APIRouter()

# ---------------------------
# Load model + Gemini
# ---------------------------

fertilizer_model_path = hf_hub_download(
    repo_id="adityaarun1010/my-new-models",
    filename="fertilizer_model.pkl"
)

model, columns = joblib.load(fertilizer_model_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------------------
# Pydantic schemas
# ---------------------------
class FertilizerRequest(BaseModel):
    Temperature: int
    Humidity: int
    Moisture: int
    Soil_Type: str
    Crop_Type: str
    Nitrogen: int
    Phosphorus: int
    Potassium: int

class RawRequest(BaseModel):
    user_input: str

# ---------------------------
# Helper functions
# ---------------------------
def clean_input_with_gemini(user_input: str) -> dict:
    """Extract structured JSON from raw text using Gemini."""
    prompt = (
        user_input
        + "\nExtract the following fields and return ONLY valid JSON:\n"
        "{\n"
        "  \"Temperature\": <int>,\n"
        "  \"Humidity\": <int>,\n"
        "  \"Moisture\": <int>,\n"
        "  \"Soil_Type\": <string>,\n"
        "  \"Crop_Type\": <string>,\n"
        "  \"Nitrogen\": <int>,\n"
        "  \"Phosphorus\": <int>,\n"
        "  \"Potassium\": <int>\n"
        "}"
    )

    response = gemini_model.generate_content(prompt)
    match = re.search(r'\{[\s\S]*\}', response.text)
    if not match:
        raise ValueError("No JSON object found in Gemini response.")
    return json.loads(match.group(0))


def predict_fertilizer(input_data: dict):
    """Run ML model prediction from structured input."""
    new_data = pd.DataFrame([input_data])
    new_data = pd.get_dummies(new_data)
    new_data = new_data.reindex(columns=columns, fill_value=0)
    return model.predict(new_data)[0]

# ---------------------------
# API endpoints
# ---------------------------
@router.post("/predict")
def predict(data: FertilizerRequest):
    input_dict = data.dict()
    prediction = predict_fertilizer(input_dict)
    return {"prediction": prediction}

@router.post("/predict_from_text")
def predict_from_text(data: RawRequest):
    try:
        structured_data = clean_input_with_gemini(data.user_input)
        prediction = predict_fertilizer(structured_data)
        return {"prediction": prediction, "parsed_data": structured_data}
    except Exception as e:
        return {"error": str(e)}
