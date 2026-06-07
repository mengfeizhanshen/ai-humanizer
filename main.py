from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from config import HOST, PORT, DEBUG, INTENSITY_LEVELS, MAX_BATCH_SIZE, MAX_TEXT_LENGTH
from humanizer import TextHumanizer
import uvicorn

app = FastAPI(
    title="AI Humanizer API",
    description="Convert AI-generated text to natural human-style writing",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Humanizer
humanizer = TextHumanizer()

# Request Models
class HumanizeRequest(BaseModel):
    text: str = Field(..., max_length=MAX_TEXT_LENGTH, description="Text to humanize")
    intensity: str = Field(default="medium", description="Intensity level: light, medium, strong")

class HumanizeBatchRequest(BaseModel):
    texts: List[str] = Field(..., max_items=MAX_BATCH_SIZE, description="List of texts to humanize")
    intensity: str = Field(default="medium", description="Intensity level: light, medium, strong")

# Response Models
class HumanizeResponse(BaseModel):
    original: str
    humanized: str
    intensity: str
    score: float

class HumanizeBatchResponse(BaseModel):
    results: List[HumanizeResponse]
    total: int
    success_count: int

class HealthResponse(BaseModel):
    status: str
    version: str

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.post("/humanize", response_model=HumanizeResponse)
async def humanize(request: HumanizeRequest):
    """Humanize a single text"""
    try:
        # Validate intensity
        if request.intensity not in INTENSITY_LEVELS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid intensity. Allowed values: {list(INTENSITY_LEVELS.keys())}"
            )
        
        # Process text
        result = humanizer.humanize(
            text=request.text,
            intensity=request.intensity
        )
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/humanize-batch", response_model=HumanizeBatchResponse)
async def humanize_batch(request: HumanizeBatchRequest):
    """Humanize multiple texts in batch"""
    try:
        # Validate intensity
        if request.intensity not in INTENSITY_LEVELS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid intensity. Allowed values: {list(INTENSITY_LEVELS.keys())}"
            )
        
        # Validate batch size
        if len(request.texts) > MAX_BATCH_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Batch size exceeds maximum limit of {MAX_BATCH_SIZE}"
            )
        
        # Process batch
        results = []
        for text in request.texts:
            result = humanizer.humanize(
                text=text,
                intensity=request.intensity
            )
            results.append(result)
        
        return {
            "results": results,
            "total": len(request.texts),
            "success_count": len(results)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/intensity-levels")
async def get_intensity_levels():
    """Get available intensity levels and their descriptions"""
    return {
        "available_levels": [
            {
                "name": name,
                "description": config["description"]
            }
            for name, config in INTENSITY_LEVELS.items()
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
