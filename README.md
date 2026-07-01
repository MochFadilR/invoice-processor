## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install pdfplumber pydantic requests tenacity reportlab
```

## Usage

Generate sample invoices for testing:
```bash
python generate_samples.py
```

Run the processor:
```bash
python src/main.py
```

Logs are saved to `logs/invoice_processor.log`.

## How It Works

1. Scans the `samples/` folder for PDF files
2. Extracts text from each PDF using `pdfplumber`
3. Parses fields using regex patterns
4. Validates data with a Pydantic model
5. Checks for duplicate invoice numbers before submitting
6. Submits valid invoices to the configured REST API endpoint
7. Retries automatically on network errors (timeout, connection error) up to 3 times

## Error Handling

| Scenario | Behavior |
|---|---|
| Missing required field | Invoice skipped, error logged |
| Missing optional field (customer name) | Submitted with null value, warning logged |
| Duplicate invoice number | Skipped, warning logged |
| API timeout / connection error | Retried up to 3 times with exponential backoff |
| API 4xx error | Skipped immediately, error logged |