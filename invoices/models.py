from django.db import models
from django.core.exceptions import ValidationError

class Invoice(models.Model):
    """This is the model for invoice"""
    date = models.DateField()
    customer_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Invoice {self.id}"

    def clean(self):
        """
        Custom validation for the Invoice model.
        """
        if self.date is None:
            raise ValidationError("Invoice date cannot be empty.")

class InvoiceDetail(models.Model):
    """This is the model for invoice detail"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="details")
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Detail for Invoice {self.invoice_id}"

    def clean(self):
        """
        Custom validation for the InvoiceDetail model.
        """

        if self.unit_price <= 0:
            raise ValidationError("Unit price must be a positive decimal number.")
        
    

    def save(self, *args, **kwargs):
        # Calculate the price based on quantity and unit_price
        self.price = self.quantity * self.unit_price
        super(InvoiceDetail, self).save(*args, **kwargs)
