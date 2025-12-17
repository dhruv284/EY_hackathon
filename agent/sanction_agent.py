from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date
import io

app = FastAPI(title="Sanction Agent")

class SanctionRequest(BaseModel):
    customer_id: str
    loan_amount: int
    interest_rate: float

@app.post("/sanction")
def generate_sanction(req: SanctionRequest):
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Watermark
    c.saveState()
    c.setFont("Helvetica-Bold", 60)
    c.setFillGray(0.9)
    c.translate(300, 250)
    c.rotate(45)
    c.drawCentredString(0, 0, "META_MINDS")
    c.restoreState()

    # Header
    c.setFont("Helvetica-Bold", 20)
    c.setFillGray(0)
    c.drawString(50, height - 80, "PROMPT_PIRATES FINANCIAL SERVICES")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 110, "AI-Driven Loan Origination Platform")
    c.line(50, height - 120, width - 50, height - 120)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 160, "LOAN SANCTION LETTER")

    y = height - 210
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Customer ID: {req.customer_id}")
    y -= 25
    c.drawString(50, y, f"Sanctioned Loan Amount: ₹{req.loan_amount}")
    y -= 25
    c.drawString(50, y, f"Interest Rate: {req.interest_rate}% per annum")
    y -= 25
    c.drawString(50, y, f"Sanction Date: {date.today()}")

    y -= 40
    c.drawString(50, y, "We are pleased to inform you that your loan application has been approved.")
    y -= 20
    c.drawString(50, y, "This sanction is issued subject to internal risk policies.")

    y -= 60
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Digitally Signed & Authorized By")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "META_MINDS Credit Decision Engine")

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 50, "System generated document. No signature required.")

    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=sanction_{req.customer_id}.pdf"
        }
    )

@app.get("/health")
def health():
    return {"status": "ok"}
