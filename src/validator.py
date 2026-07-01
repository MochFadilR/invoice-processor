from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date
import logging

logger = logging.getLogger(__name__)

class Invoice(BaseModel):
    invoice_number: str
    date: date
    customer_name: Optional[str] = None
    total_amount: float

    @field_validator("total_amount", mode="before")
    @classmethod
    def parse_amount(cls, v):
        try:
            return float(v)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid total_amount: {v}")

    @field_validator("customer_name", mode="before")
    @classmethod
    def check_customer_name(cls, v):
        if not v or v.strip() == "":
            logger.warning("customer_name is empty, setting to None")
            return None
        return v

def validate_invoice(raw: dict) -> tuple[Invoice | None, list[str]]:
    errors = []

    try:
        invoice = Invoice(**raw)
        return invoice, errors
    except Exception as e:
        for err in e.errors():
            field = " -> ".join(str(x) for x in err["loc"])
            errors.append(f"{field}: {err['msg']}")
        return None, errors

# if __name__ == "__main__":
#     from extractor import extract_invoice_data

#     test_cases = ["samples/INV-001.pdf", "samples/INV-003.pdf"]

#     for path in test_cases:
#         raw = extract_invoice_data(path)
#         invoice, errors = validate_invoice(raw)
#         print(f"\n--- {path} ---")
#         if invoice:
#             print(invoice.model_dump())
#         else:
#             print(f"Validation failed: {errors}")