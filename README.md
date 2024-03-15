# Assignment

This Django application is created to manage invoices and invoice details. Below are the details and requirements for this assignment:

### URL Endpoints:
- `/invoices/`
- `/invoices/<int:pk>/`

### Models:
1. **Invoice Model:**
   - Fields: Date, Invoice CustomerName

2. **InvoiceDetail Model:**
   - Fields: invoice (ForeignKey to Invoice model), description, quantity, unit_price, price

### APIs:
- Create APIs using Django Rest Framework for all HTTP methods for the invoice models.

### Test Cases:
- Test cases to ensure proper functionality and data integrity.
