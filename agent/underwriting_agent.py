from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Underwriting Agent")

class UnderwriteRequest(BaseModel):
    customer_id: str
    credit_score: int
    loan_amount: int

@app.post("/underwrite")
def underwrite(req: UnderwriteRequest):
    if req.credit_score >= 720 and req.loan_amount <= 300000:
        return {
            "customer_id": req.customer_id,
            "approved": True,
            "reason": "Eligible as per underwriting rules"
        }

    return {
        "customer_id": req.customer_id,
        "approved": False,
        "reason": "Credit risk too high"
    }

@app.get("/uagent")
def root():
    return {"status": "Underwriting Agent running"}
