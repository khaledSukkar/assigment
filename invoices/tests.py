from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Invoice

class InvoiceViewSetTests(APITestCase):
    def test_create_invoice_valid(self):
        url = reverse('invoice-list')
        data = {
            'date': '2024-03-16',
            'customer_name': 'John Doe',
            'details': [
                {'description': 'Product A', 'quantity': 2, 'unit_price': 10.0},
                {'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['customer_name'], 'John Doe')

    def test_create_invoice_invalid_date(self):
        url = reverse('invoice-list')
        data = {
            'date': '2024-03-17', # Future date
            'customer_name': 'John Doe',
            'details': [
                {'description': 'Product A', 'quantity': 2, 'unit_price': 10.0},
                {'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_short_customer_name(self):
        url = reverse('invoice-list')
        data = {
            'date': '2024-03-16',
            'customer_name': 'Jo', # Short name
            'details': [
                {'id':3 ,'description': 'Product A', 'quantity': 2, 'unit_price': 10.0},
                {'id':4,'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_detail_valid(self):
        invoice = Invoice.objects.create(date='2024-03-16', customer_name='John Doe')
        url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        data = {
            'details': [
                {'description': 'Product A', 'quantity': 2, 'unit_price': 10.0},
                {'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['details']), 2)

    def test_create_invoice_detail_negative_quantity(self):
        invoice = Invoice.objects.create(date='2024-03-16', customer_name='John Doe')
        url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        data = {
            'details': [
                {'description': 'Product A', 'quantity': -2, 'unit_price': 10.0}, # Negative quantity
                {'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_detail_negative_unit_price(self):
        invoice = Invoice.objects.create(date='2024-03-16', customer_name='John Doe')
        url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        data = {
            'details': [
                {'description': 'Product A', 'quantity': 2, 'unit_price': -10.0}, # Negative unit price
                {'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_with_details_correct_total_price(self):
        invoice = Invoice.objects.create(date='2024-03-16', customer_name='John Doe')
        url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        data = {
            'details': [
                {'description': 'Product A', 'quantity': 2, 'unit_price': 10.0},
                {'description': 'Product B', 'quantity': 1, 'unit_price': 20.0}
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['details'][0]['price']), 20.0)
        self.assertEqual(float(response.data['details'][1]['price']), 20.0)

    def test_invoice_with_details_and_invalid_detail(self):
        invoice = Invoice.objects.create(date='2024-03-16', customer_name='John Doe')
        url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        data = {
            'details': [
                {'description': 'Product A', 'quantity': 2, 'unit_price': 10.0},
                {'description': 'Product B', 'quantity': -1, 'unit_price': 20.0} # Invalid detail
            ]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invoice_with_empty_details(self):
        invoice = Invoice.objects.create(date='2024-03-16', customer_name='John Doe')
        url = reverse('invoice-detail', kwargs={'pk': invoice.pk})
        data = {
            'details': []
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    