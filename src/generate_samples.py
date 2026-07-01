from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate(filename, data):
    os.makedirs("samples", exist_ok=True)
    c = canvas.Canvas(f"samples/{filename}", pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Invoice Number: {data['invoice_number']}")
    c.drawString(50, height - 120, f"Date: {data['date']}")
    c.drawString(50, height - 140, f"Customer Name: {data['customer_name']}")
    c.drawString(50, height - 160, f"Total Amount: EUR {data['total_amount']}")
    c.save()
    print(f"Generated: samples/{filename}")

invoices = [
    ("INV-001.pdf",           {"invoice_number": "INV-001", "date": "2024-01-15", "customer_name": "Acme Corp", "total_amount": "1500.00"}),
    ("INV-002.pdf",           {"invoice_number": "INV-002", "date": "2024-01-20", "customer_name": "Beta LLC",  "total_amount": "320.50"}),
    ("INV-001-duplicate.pdf", {"invoice_number": "INV-001", "date": "2024-01-15", "customer_name": "Acme Corp", "total_amount": "1500.00"}),
    ("INV-003.pdf",           {"invoice_number": "INV-003", "date": "2024-01-22", "customer_name": "",          "total_amount": "750.00"}),
]

for filename, data in invoices:
    generate(filename, data)