from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sales Agent")

class SalesRequest(BaseModel):
    customer_id: str
    credit_score: int

@app.post("/sales/recommend")
def recommend_offer(req: SalesRequest):
    if req.credit_score >= 750:
        return {
            "customer_id": req.customer_id,
            "loan_limit": 500000,
            "interest_rate": 11.5,
            "tenure_months": [12, 24, 36]
        }

    if req.credit_score >= 700:
        return {
            "customer_id": req.customer_id,
            "loan_limit": 300000,
            "interest_rate": 12.5,
            "tenure_months": [12, 24]
        }

    return {
        "customer_id": req.customer_id,
        "loan_limit": 100000,
        "interest_rate": 15.5,
        "tenure_months": [12]
    }

@app.get("/")
def root():
    return {"status": "Sales Agent running"}
