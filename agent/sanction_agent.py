from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = FastAPI(title="Sanction Agent")

SANCTION_DIR = "sanction_letters"
os.makedirs(SANCTION_DIR, exist_ok=True)

class SanctionRequest(BaseModel):
    customer_id: str
    loan_amount: int
    interest_rate: float

@app.post("/sanction")
def generate_sanction_letter(req: SanctionRequest):
    today = date.today().strftime("%d-%m-%Y")
    file_name = f"sanction_{req.customer_id}.pdf"
    file_path = os.path.join(SANCTION_DIR, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "LOAN SANCTION LETTER")

    c.setFont("Helvetica", 11)
    c.drawString(50, height - 100, f"Date: {today}")
    c.drawString(50, height - 130, f"Customer ID: {req.customer_id}")
    c.drawString(50, height - 160, f"Loan Amount: ₹{req.loan_amount}")
    c.drawString(50, height - 190, f"Interest Rate: {req.interest_rate}% per annum")

    c.drawString(50, height - 240, "Dear Customer,")
    c.drawString(
        50,
        height - 270,
        "We are pleased to inform you that your personal loan has been approved."
    )

    c.drawString(
        50,
        height - 300,
        "Please find the loan terms above. This sanction is subject to final verification."
    )

    c.drawString(50, height - 360, "Sincerely,")
    c.drawString(50, height - 390, "Loan Operations Team")

    c.showPage()
    c.save()

    return {
        "status": "SANCTIONED",
        "sanction_letter": file_path
    }

@app.get("/health")
def health():
    return {"status": "ok"}
