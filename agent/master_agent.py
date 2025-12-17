from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
impo
app = FastAPI(title="Master Agent")

VERIFICATION_URL = os.getenv("VERIFICATION_URL")
SALES_URL = os.getenv("SALES_URL")
UNDERWRITING_URL = os.getenv("UNDERWRITING_URL")
SANCTION_URL = os.getenv("SANCTION_URL")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    customer_id: str
    pan: str
    full_name: str
    phone: str
    requested_amount: int


@app.post("/apply-loan")
async def apply_loan(req: LoanRequest):
    async with httpx.AsyncClient() as client:

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
        verification = verification_resp.json()

        # ❌ REJECT
        if verification["decision"] == "REJECTED":
            return {
                "status": "REJECTED",
                "reason": verification["reason"],
                "credit_score": verification["credit_score"]
            }

        # ⚠️ NEED AADHAAR
        if verification["decision"] == "MORE_DETAILS_REQUIRED":
            return {
                "status": "PENDING",
                "required_fields": verification["required_fields"],
                "next_step": {
                    "endpoint": "http://localhost:9004/verify/aadhaar",
                    "method": "POST",
                    "description": "Upload Aadhaar to continue"
                }
            }

        # ✅ APPROVED
        credit_score = verification["credit_score"]

        # 2️⃣ SALES
        sales_resp = await client.post(
            f"{SALES_URL}/sales/recommend",
            json={
                "customer_id": req.customer_id,
                "credit_score": credit_score
            }
        )
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
        uw = underwriting_resp.json()

        if not uw["approved"]:
            return {
                "status": "REJECTED",
                "reason": uw["reason"]
            }

        # 4️⃣ SANCTION
        sanction_resp = await client.post(
            f"{SANCTION_URL}/sanction",
            json={
                "customer_id": req.customer_id,
                "loan_amount": req.requested_amount,
                "interest_rate": offer["interest_rate"]
            }
        )

        return {
            "status": "APPROVED",
            "sanction": sanction_resp.json()
        }


@app.get("/")
def root():
    return {"status": "Master Agent running"}


@app.get("/health")
def health():
    return {"status": "ok"}
