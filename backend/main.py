from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables (from .env inside backend/)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Debug print (remove later if not needed)
print(f"DEBUG: PRIVATE_KEY starts with: {str(os.getenv('PRIVATE_KEY'))[:25]}...")

# Import routers
from FarmAgent.routes import router as farm_router
from Plant_Disease.routes import router as plant_router
from FertilizerSuggestor.routes import router as fert_router
from Yield_Prediction.routes import router as yield_router

# Create FastAPI app
app = FastAPI(
    title="Unified Backend",
    description="Single backend server for FarmAgent, Plant_Disease and other services",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(farm_router, prefix="/farm", tags=["FarmAgent"])
app.include_router(plant_router, prefix="/plant", tags=["Plant_Disease"])
app.include_router(fert_router, prefix="/fertilizer", tags=["FertilizerSuggestor"])
app.include_router(yield_router, prefix="/yield", tags=["YieldPredictor"])

@app.get("/")
def root():
    return {"message": "Unified Backend running successfully"}

# Only for local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",   # ✅ correct since Render root is backend/
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=not os.getenv("RENDER")  # ✅ reload locally, disabled on Render
    )
