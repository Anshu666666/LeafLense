import tensorflow as tf
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
from tensorflow import keras
from huggingface_hub import hf_hub_download
# from langchain_google_genai import ChatGoogleGenerativeAI  # Temporarily disabled
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
# Use tf.keras instead of standalone keras

# ✅ Router for Plant Disease
router = APIRouter(prefix="/disease", tags=["Plant Disease"])

# ✅ Class labels
class_names = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

# ✅ Path to trained model
keras_path = hf_hub_download(
    repo_id="adityaarun1010/my-new-models",
    filename="trained_model.keras"
)

# ✅ Load model with fallback to mock model for development
try:
    print(f"\n🔄 Loading model from: {keras_path}")
    
    # First try: tf.saved_model.load (works with Keras 3 for inference)
    try:
        model = tf.saved_model.load(keras_path)
        print("\n✅ Model loaded successfully using tf.saved_model.load")
        print(f"📊 Model signatures: {list(model.signatures.keys())}")
        model_type = "saved_model"
    except Exception as e1:
        print(f"\n⚠️ tf.saved_model.load failed: {e1}")
        
        # Second try: TFSMLayer
        try:
            import keras
            model = keras.layers.TFSMLayer(MODEL_PATH, call_endpoint='serving_default')
            print("\n✅ Model loaded successfully using TFSMLayer")
            model_type = "tfsm_layer"
        except Exception as e2:
            print(f"\n⚠️ TFSMLayer also failed: {e2}")
            
            # Fallback: Create a mock model for development/testing
            print("\n🔄 Creating mock model for development/testing...")
            
            # Create a simple mock model that returns realistic predictions
            class MockModel:
                def __init__(self):
                    self.num_classes = len(class_names)
                    print(f"📊 Mock model created with {self.num_classes} classes")
                
                def predict(self, input_arr):
                    # Return random but realistic predictions
                    np.random.seed(42)  # For consistent results during development
                    predictions = np.random.dirichlet(np.ones(self.num_classes) * 0.1, size=1)
                    # Boost one class to simulate a detection
                    max_idx = np.random.randint(0, self.num_classes)
                    predictions[0][max_idx] *= 5  # Make one class more likely
                    predictions = predictions / np.sum(predictions, axis=1, keepdims=True)  # Renormalize
                    print(f"📊 Mock prediction generated, max confidence: {np.max(predictions):.3f}")
                    return predictions
            
            model = MockModel()
            model_type = "mock"
            print("\n✅ Mock model created successfully for testing")
            print("⚠️ Note: This is a temporary mock model for development.")
            print("📝 To use the real model, please retrain it with TensorFlow 2.17+ or provide a compatible .keras file")
            
except Exception as e:
    print(f"\n❌ Unexpected error during model loading: {e}")
    model = None
    model_type = "none"

# ✅ Gemini setup (temporarily disabled - requires Google API credentials)
# from langchain_google_genai import ChatGoogleGenerativeAI
# gemini_llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     temperature=0.5,
#     max_tokens="200"
# )
# parser = StrOutputParser()
gemini_llm = None  # Temporary placeholder
parser = None

prompt1 = PromptTemplate(
    template="""
        You are an agriculture expert. 
        A farmer's plant or leaf has the disease: {disease}.
        Suggest:
        1. Short description of the disease
        2. Organic remedies
        3. Chemical remedies (if available)
        4. Preventive measures
        Return the answer in simple and matured and respected language and answer should be within 100 words.
        You should return the answer in such a manner:
        ### Disease Name
        ---
        ### Cause
        --- (if any)
        ### Symptoms
        --- (if any)

        ### Organic Remedies
        ---  (if any)

        ### Chemical Remedies
        --- (if any) 

        ### Prevention
        --- (if any)
        and never try highlighting any text using **. so give proper response.
    """,
    input_variables=["disease"]
)
chain1 = None  # Temporarily disabled until Gemini credentials are set up

# ✅ Prediction endpoint
@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse(content={"error": "Model not loaded."}, status_code=500)

    try:
        # Read and preprocess image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Resize to model input size
        image = image.resize((128, 128))
        
        # Convert to array and normalize
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = input_arr / 255.0  # Normalize pixel values
        input_arr = np.expand_dims(input_arr, axis=0)
        
        print(f"📊 Input shape: {input_arr.shape}")

        # Make prediction based on model type
        global model_type
        if model_type == "mock":
            prediction = model.predict(input_arr)
        elif model_type == "saved_model":
            # Handle tf.saved_model.load predictions
            if 'serving_default' in model.signatures:
                infer = model.signatures["serving_default"]
            else:
                sig_key = list(model.signatures.keys())[0]
                infer = model.signatures[sig_key]
            
            input_keys = list(infer.structured_input_signature[1].keys())
            input_key = input_keys[0] if input_keys else 'input_1'
            
            prediction_dict = infer(**{input_key: tf.constant(input_arr, dtype=tf.float32)})
            output_keys = list(prediction_dict.keys())
            prediction = prediction_dict[output_keys[0]].numpy()
        elif model_type == "tfsm_layer":
            # Handle TFSMLayer predictions
            prediction = model(input_arr)
            if isinstance(prediction, dict):
                prediction_key = list(prediction.keys())[0]
                prediction = prediction[prediction_key].numpy()
            else:
                prediction = prediction.numpy()
        else:
            # Fallback prediction method
            prediction = model.predict(input_arr)
        
        print(f"📊 Prediction shape: {prediction.shape}")
        print(f"📊 Prediction values: {prediction[0][:5]}...")  # Show first 5 values
        
        result_index = np.argmax(prediction, axis=1)[0]
        confidence = float(prediction[0][result_index])
        
        print(f"📊 Predicted class index: {result_index}")
        print(f"📊 Confidence: {confidence:.4f}")

        if confidence < 0.5:  # Lower threshold for testing
            result = "Unknown Disease (Low confidence)"
            disease_advice = "The confidence level is too low to make a reliable prediction. Please ensure the image is clear, well-lit, and shows visible disease symptoms on the plant leaf."
        else:
            result = class_names[result_index]
            # Generate basic advice based on disease type
            if "healthy" in result.lower():
                disease_advice = "Good news! Your plant appears to be healthy. Continue with regular care and monitoring."
            elif "unknown" in result.lower():
                disease_advice = "Unable to identify the specific disease. Please consult with a local agricultural expert for proper diagnosis."
            else:
                disease_advice = f"Disease detected: {result}. Please consult with a local agricultural expert for specific treatment recommendations."

        # AI advice (temporarily using simple rule-based advice)
        ai_response = disease_advice
        if model_type == "mock":
            ai_response += "\n\n⚠️ Note: This prediction is from a mock model for development testing. For real disease detection, please provide a properly trained model."

        return {
            "class": result,
            "confidence": round(confidence * 100, 2),  # Convert to percentage
            "advice": ai_response,
            "model_type": model_type,
            "status": "success",
            "all_predictions": prediction[0].tolist()[:10]  # Show top 10 predictions for debugging
        }

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(content={
            "error": f"Prediction failed: {str(e)}",
            "status": "error"
        }, status_code=500)
