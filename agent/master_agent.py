import httpx
from fastapi import FastAPI
from pydantic import BaseModel
import os
app = FastAPI(title="Master Agent")

VERIFICATION_URL = os.getenv("VERIFICATION_URL")
SALES_URL = os.getenv("SALES_URL")
UNDERWRITING_URL = os.getenv("UNDERWRITING_URL")
SANCTION_URL = os.getenv("SANCTION_URL")

class LoanRequest(BaseModel):
    customer_id: str
    pan: str
    full_name: str
    phone: str
    requested_amount: int

@app.post("/apply-loan")
async def apply_loan(req: LoanRequest):
    async with httpx.AsyncClient() as client:
        verification = await client.post(
            f"{VERIFICATION_URL}/verify",
            json=req.dict()
        )
        v = verification.json()

        if not v["verification_passed"]:
            return {"status": "REJECTED", "reason": "Verification failed"}

        sales = await client.post(
            f"{SALES_URL}/sales/recommend",
            json={
                "customer_id": req.customer_id,
                "credit_score": v["credit_score"]
            }
        )
        offer = sales.json()

        underwriting = await client.post(
            f"{UNDERWRITING_URL}/underwrite",
            json={
                "customer_id": req.customer_id,
                "credit_score": v["credit_score"],
                "loan_amount": req.requested_amount
            }
        )
        uw = underwriting.json()

        if not uw["approved"]:
            return {"status": "REJECTED", "reason": uw["reason"]}

        sanction = await client.post(
            f"{SANCTION_URL}/sanction",
            json={
                "customer_id": req.customer_id,
                "loan_amount": req.requested_amount,
                "interest_rate": offer["interest_rate"]
            }
        )

        return {
            "status": "APPROVED",
            "sanction": sanction.json()
        }

@app.get("/")
def root():
    return {"status": "Master Agent running"}
