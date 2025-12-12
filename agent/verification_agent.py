# agent/verification_agent.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Verification Agent")

# Load endpoints from environment variables
CRM_URL = os.getenv("CRM_URL")
CREDIT_URL = os.getenv("CREDIT_URL")
OFFER_URL = os.getenv("OFFER_URL")  # optional

if not CRM_URL or not CREDIT_URL:
    # in Render you'll set env vars; locally you can use .env or export them
    # we still allow starting but warn in logs (no print in FastAPI startup here)
    pass


class VerifyRequest(BaseModel):
    customer_id: str
    pan: str
    full_name: str
    phone: str


@app.post("/verify")
async def verify(req: VerifyRequest):
    # use a reasonable timeout
    timeout = httpx.Timeout(5.0, read=10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Get CRM
        try:
            crm_resp = await client.get(f"{CRM_URL}/crm/{req.customer_id}")
            crm_resp.raise_for_status()
            crm = crm_resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise HTTPException(status_code=404, detail="Customer not found in CRM")
            raise HTTPException(status_code=502, detail="CRM returned an error")
        except Exception:
            raise HTTPException(status_code=502, detail="Failed to reach CRM")

        # Get Credit
        try:
            credit_resp = await client.get(f"{CREDIT_URL}/credit/{req.pan}")
            credit_resp.raise_for_status()
            credit = credit_resp.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail="Credit service returned an error")
        except Exception:
            raise HTTPException(status_code=502, detail="Failed to reach Credit service")

        # Optionally get offers (non-blocking failure)
        offers = None
        if OFFER_URL:
            try:
                offers_resp = await client.get(f"{OFFER_URL}/offers/{req.customer_id}")
                if offers_resp.status_code == 200:
                    offers = offers_resp.json()
            except Exception:
                offers = None

    result = {
        "pan_match": crm.get("pan") == req.pan,
        "name_match": crm.get("full_name", "").strip().lower() == req.full_name.strip().lower(),
        "phone_match": crm.get("phone") == req.phone,
        "credit_score": credit.get("credit_score", 0),
        "offers": offers
    }

    result["verification_passed"] = (
        result["pan_match"]
        and result["name_match"]
        and result["phone_match"]
        and result["credit_score"] >= 700
    )

    return result


@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/")
def root():
    return {"message": "Mock Services API is running", "status": "ok"}