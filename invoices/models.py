from django.db import models

# Create your models here.
class Invoice(models.Model):
    """This is the model for invoice"""
    date = models.DateField()
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Invoice {self.id}"


class InvoiceDetail(models.Model):
    """This is the model for invoice detail"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="details")
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for Invoice {self.invoice_id}"