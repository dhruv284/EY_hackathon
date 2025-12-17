from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date
import os

app = FastAPI(title="Sanction Agent")

BASE_DIR = "sanction_letters"
os.makedirs(BASE_DIR, exist_ok=True)

class SanctionRequest(BaseModel):
    customer_id: str
    loan_amount: int
    interest_rate: float

@app.post("/sanction")
def generate_sanction(req: SanctionRequest):
    file_name = f"sanction_{req.customer_id}.pdf"
    file_path = os.path.join(BASE_DIR, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.saveState()
    c.setFont("Helvetica-Bold", 60)
    c.setFillGray(0.9)
    c.translate(300, 250)
    c.rotate(45)
    c.drawCentredString(0, 0, "META_MINDS")
    c.restoreState()

    c.setFont("Helvetica-Bold", 20)
    c.setFillGray(0)
    c.drawString(50, height - 80, "META_MINDS FINANCIAL SERVICES")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 110, "AI-Driven Loan Origination Platform")

    c.line(50, height - 120, width - 50, height - 120)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 160, "LOAN SANCTION LETTER")

    c.setFont("Helvetica", 12)
    y = height - 210

    c.drawString(50, y, f"Customer ID: {req.customer_id}")
    y -= 25
    c.drawString(50, y, f"Sanctioned Loan Amount: ₹{req.loan_amount}")
    y -= 25
    c.drawString(50, y, f"Interest Rate: {req.interest_rate}% per annum")
    y -= 25
    c.drawString(50, y, f"Sanction Date: {date.today()}")

    y -= 40
    c.setFont("Helvetica", 11)
    c.drawString(50, y, "We are pleased to inform you that your loan application has been")
    y -= 20
    c.drawString(50, y, "successfully approved based on AI-driven credit verification and underwriting.")

    y -= 30
    c.drawString(50, y, "This sanction is issued subject to internal risk policies and regulatory compliance.")

    y -= 60
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Digitally Signed & Authorized By")

    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "META_MINDS Credit Decision Engine")

    y -= 20
    c.drawString(50, y, f"Date: {date.today()}")

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        50,
        50,
        "This is a system-generated sanction letter and does not require a physical signature."
    )

    c.save()

    return {
        "status": "SANCTIONED",
        "sanction_letter": f"/download/{file_name}"
    }

@app.get("/download/{file_name}")
def download(file_name: str):
    file_path = os.path.join(BASE_DIR, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sanction letter not found")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_name
    )

@app.get("/health")
def health():
    return {"status": "ok"}
