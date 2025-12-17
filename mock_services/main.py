# mock_services/main.py
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Mock Services (CRM / Credit / Offers)")

MOCK_CRM = {
    "C001": {
        "full_name": "Akshay Choudhary",
        "phone": "9876543210",
        "address": "Rourkela",
        "pan": "ABCDE1234F",
        "kyc_status": "VERIFIED"
    },
    "C009": {
        "full_name": "Test User",
        "phone": "9000000001",
        "address": "Bangalore",
        "pan": "PAN_MID_001",
        "kyc_status": "PENDING"
    }
}


MOCK_CREDIT = {
    "ABCDE1234F": {"credit_score": 760},
    "XYZ9876543": {"credit_score": 650},
    "PAN1234567": {"credit_score": 720},
    "PAN_MID_001": {"credit_score":600}
}

MOCK_OFFERS = {
    "C001": {
        "pre_approved_limit": 300000,
        "offers": [
            {
                "product_id": "PL_BASIC",
                "rate": 12.0,
                "tenures": [12, 24, 36]
            }
        ]
    }
}


@app.get("/crm/{customer_id}")
def get_customer(customer_id: str):
    data = MOCK_CRM.get(customer_id)
    if not data:
        raise HTTPException(status_code=404, detail="Customer not found")
    return data


@app.get("/credit/{pan}")
def get_credit(pan: str):
    # default credit score if not present
    return MOCK_CREDIT.get(pan, {"credit_score": 600})


@app.get("/offers/{customer_id}")
def get_offers(customer_id: str):
    data = MOCK_OFFERS.get(customer_id)
    if not data:
        raise HTTPException(status_code=404, detail="No offers found")
    return data


@app.get("/health")
def health():
    return {"status": "ok"}
