import math

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scoring_api import evaluate
from phase2.optimization import IterativeOptimizer

app = FastAPI(title="AI Code Maintainability Scoring Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScoreRequest(BaseModel):
    code: str


class RefactorRequest(BaseModel):
    code: str
    target_score: float = 20.0
    max_iterations: int = 3


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/score")
def score(request: ScoreRequest):
    return evaluate(request.code)


@app.post("/api/refactor")
def refactor(request: RefactorRequest):
    optimizer = IterativeOptimizer(
        target_score=request.target_score,
        max_iterations=request.max_iterations,
    )
    result = optimizer.optimize(request.code)
    if not math.isfinite(result["final_score"]):
        result["final_score"] = None
    return result
