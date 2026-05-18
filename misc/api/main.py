from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import pickle, os
import pandas as pd

app = FastAPI(
    title="Lung Cancer Risk Prediction API",
    version="1.0.0"
)

class PredictionRequest(BaseModel):
    age:                int   = Field(..., ge=0, le=120, example=55)
    country:            str   = Field(..., example="Japan")
    gender:             Literal["Male", "Female"] = Field(..., example="Male")
    smoker:             Literal["Yes", "No"] = Field(..., example="Yes")
    years_of_smoking:   int   = Field(..., ge=0, example=20)
    cigarettes_per_day: int   = Field(..., ge=0, example=15)

class PredictionResponse(BaseModel):
    risk_score:    float
    risk_label:    str
    model_version: str

def score_to_label(score: float) -> str:
    if score < 0.4:  return "Low"
    if score < 0.65: return "Medium"
    return "High"

def rule_based_score(req: PredictionRequest) -> float:
    score = 0.1
    if req.smoker == "Yes":
        score += 0.35
        score += min(req.years_of_smoking * 0.008, 0.25)
        score += min(req.cigarettes_per_day * 0.005, 0.15)
    if req.gender == "Male":
        score += 0.05
    return min(round(score, 4), 1.0)

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    score = rule_based_score(request)
    return PredictionResponse(
        risk_score=score,
        risk_label=score_to_label(score),
        model_version="1.0"
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/data/risk_by_country")
def get_risk_by_country():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(base_dir, "data", "risk_by_country.csv")

    if not os.path.exists(csv_path):
        return {"error": f"File not found at {csv_path}"}
    
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")


@app.get("/")
async def root():
    return {"message": "Lung Cancer Risk API — visit /docs"}