from rest_framework import viewsets
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    This is the ViewSet for Invoice model
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceDetailViewSet(viewsets.ModelViewSet):
    """
    This is thte Viewset for Invoice detail model
    """
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer