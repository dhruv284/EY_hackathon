from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import os
import io

app = FastAPI(title="Master Agent")

# Environment variables
VERIFICATION_URL = os.getenv("VERIFICATION_URL")
SALES_URL = os.getenv("SALES_URL")
UNDERWRITING_URL = os.getenv("UNDERWRITING_URL")
SANCTION_URL = os.getenv("SANCTION_URL")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class LoanRequest(BaseModel):
    customer_id: str
    pan: str
    full_name: str
    phone: str
    requested_amount: int


@app.post("/apply-loan")
async def apply_loan(req: LoanRequest):
    async with httpx.AsyncClient(timeout=30) as client:

        # 1️⃣ VERIFICATION
        verification_resp = await client.post(
            f"{VERIFICATION_URL}/verify",
            json={
                "customer_id": req.customer_id,
                "pan": req.pan,
                "full_name": req.full_name,
                "phone": req.phone
            }
        )

        if verification_resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Verification service failed")

        verification = verification_resp.json()

        # ❌ REJECTED
        if verification["decision"] == "REJECTED":
            return {
                "status": "REJECTED",
                "reason": verification.get("reason"),
                "credit_score": verification.get("credit_score")
            }

        # ⚠️ NEED MORE DETAILS
        if verification["decision"] == "MORE_DETAILS_REQUIRED":
            return {
                "status": "PENDING",
                "required_fields": verification.get("required_fields"),
                "next_step": {
                    "endpoint": "/verify/aadhaar",
                    "method": "POST",
                    "description": "Upload Aadhaar to continue"
                }
            }

        # ✅ VERIFIED
        credit_score = verification["credit_score"]

        # 2️⃣ SALES
        sales_resp = await client.post(
            f"{SALES_URL}/sales/recommend",
            json={
                "customer_id": req.customer_id,
                "credit_score": credit_score
            }
        )

        if sales_resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Sales service failed")

        offer = sales_resp.json()

        # 3️⃣ UNDERWRITING
        underwriting_resp = await client.post(
            f"{UNDERWRITING_URL}/underwrite",
            json={
                "customer_id": req.customer_id,
                "credit_score": credit_score,
                "loan_amount": req.requested_amount
            }
        )

        if underwriting_resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Underwriting service failed")

        uw = underwriting_resp.json()

        if not uw["approved"]:
            return {
                "status": "REJECTED",
                "reason": uw.get("reason")
            }

        # 4️⃣ SANCTION (PDF STREAM)
        sanction_resp = await client.post(
            f"{SANCTION_URL}/sanction",
            json={
                "customer_id": req.customer_id,
                "loan_amount": req.requested_amount,
                "interest_rate": offer["interest_rate"]
            }
        )

        if sanction_resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Sanction service failed")

        # ✅ IMPORTANT: DO NOT CALL .json()
        pdf_bytes = sanction_resp.content

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=sanction_{req.customer_id}.pdf"
            }
        )


@app.get("/")
def root():
    return {"status": "Master Agent running"}


@app.get("/health")
def health():
    return {"status": "ok"}
