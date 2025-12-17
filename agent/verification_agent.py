# agent/verification_agent.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
import httpx
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Verification Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load endpoints from environment variables
CRM_URL = os.getenv("CRM_URL")
CREDIT_URL = os.getenv("CREDIT_URL")
OFFER_URL = os.getenv("OFFER_URL")  # optional

if not CRM_URL or not CREDIT_URL:
    # in Render you'll set env vars; locally you can use .env or export them
    # we still allow starting but warn in logs (no print in FastAPI startup here)
    pass

AADHAAR_DIR = "aadhaar_uploads"
os.makedirs(AADHAAR_DIR, exist_ok=True)

class VerifyRequest(BaseModel):
    customer_id: str
    pan: str
    full_name: str
    phone: str


@app.post("/verify")
async def verify(req: VerifyRequest):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            crm_resp = await client.get(f"{CRM_URL}/crm/{req.customer_id}")
            crm_resp.raise_for_status()
            crm = crm_resp.json()

            credit_resp = await client.get(f"{CREDIT_URL}/credit/{req.pan}")
            credit_resp.raise_for_status()
            credit = credit_resp.json()
        except Exception:
            raise HTTPException(status_code=502, detail="Upstream service error")

    credit_score = credit.get("credit_score", 0)

    # ❌ RULE 1: CREDIT SCORE < 550 → REJECT
    if credit_score < 550:
        return {
            "decision": "REJECTED",
            "reason": "Credit score below 550",
            "credit_score": credit_score
        }

    # ⚠ RULE 2: CREDIT SCORE 550–699 → ASK FOR AADHAAR
    if 550 <= credit_score < 700:
        return {
            "decision": "MORE_DETAILS_REQUIRED",
            "credit_score": credit_score,
            "required_fields": ["aadhaar", "address"]
        }

    # ✅ RULE 3: CREDIT SCORE ≥ 700 → APPROVED
    offers = None
    try:
        offers_resp = httpx.get(f"{OFFER_URL}/offers/{req.customer_id}")
        if offers_resp.status_code == 200:
            offers = offers_resp.json()
    except Exception:
        offers = None

    return {
        "decision": "APPROVED",
        "credit_score": credit_score,
        "verified_data": {
            "pan": crm.get("pan"),
            "address": crm.get("address"),
            "phone": crm.get("phone"),
            "kyc_status": crm.get("kyc_status")
        },
        "offers": offers
    }


@app.post("/verify/aadhaar")
async def verify_aadhaar(
    customer_id: str = Form(...),
    aadhaar_number: str = Form(...),
    aadhaar_file: UploadFile = File(...)
):
    if len(aadhaar_number) != 12 or not aadhaar_number.isdigit():
        raise HTTPException(status_code=400, detail="Invalid Aadhaar number")

    file_path = os.path.join(
        AADHAAR_DIR,
        f"{customer_id}_{aadhaar_file.filename}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(aadhaar_file.file, buffer)

    return {
        "status": "VERIFIED",
        "message": "Aadhaar verification successful",
        "customer_id": customer_id
    }


@app.get("/health")
def health():
    return {"status": "ok"}
