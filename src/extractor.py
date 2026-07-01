import pdfplumber
import re
import logging
import json
import os

logger = logging.getLogger(__name__)

def extract_invoice_data(pdf_path: str) -> dict:
    raw = {}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    except Exception as e:
        logger.error(f"Failed to open PDF {pdf_path}: {e}")
        return raw

    patterns = {
        "invoice_number": r"Invoice Number:\s*(\S+)",
        "date": r"Date:\s*(\S+)",
        "customer_name": r"Customer Name:[ \t]*(.*?)(?:\n|$)",
        "total_amount": r"Total Amount:\s*EUR\s*([\d.]+)",
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            raw[field] = match.group(1).strip()
        else:
            raw[field] = None
            logger.warning(f"Field '{field}' not found in {pdf_path}")

    return raw

