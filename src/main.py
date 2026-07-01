import os
import json
import logging
from extractor import extract_invoice_data
from validator import validate_invoice
from api_client import submit_invoice

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/invoice_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Duplicate tracker
processed_ids = set()

def process_invoice(pdf_path: str):
    logger.info(f"Processing {pdf_path}")

    # Step 1: Extract
    raw = extract_invoice_data(pdf_path)

    # Step 2: Validate
    invoice, errors = validate_invoice(raw)
    if not invoice:
        logger.error(f"Validation failed for {pdf_path}: {errors}")
        return

    # Step 3: Duplicate check
    if invoice.invoice_number in processed_ids:
        logger.warning(f"Duplicate invoice skipped: {invoice.invoice_number}")
        return

    # Step 4: Submit to API
    success, message = submit_invoice(invoice)
    if success:
        processed_ids.add(invoice.invoice_number)
        logger.info(f"Done: {invoice.invoice_number}")
    else:
        logger.error(f"Submission failed for {invoice.invoice_number}: {message}")

def main():
    pdf_files = [f"samples/{f}" for f in os.listdir("samples") if f.endswith(".pdf")]

    if not pdf_files:
        logger.warning("No PDF files found in samples/")
        return

    logger.info(f"Found {len(pdf_files)} PDF(s) to process")

    for pdf_path in sorted(pdf_files):
        process_invoice(pdf_path)

    logger.info("All done.")

if __name__ == "__main__":
    main()