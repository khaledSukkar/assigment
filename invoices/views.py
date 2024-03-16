from rest_framework import viewsets, status, exceptions
from rest_framework.response import Response
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on Invoices and Invoice Details.
    """

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Overrides the base get_serializer method
        to dynamically set the required status of 'date' and 'customer_name' fields
        based on the request method. For PATCH requests, these fields are made optional
        """
        serializer = super().get_serializer(*args, **kwargs)
        # Check if the request is a PATCH request
        if self.request.method == 'PATCH':
            # Make 'date' and 'customer_name' not required for PATCH requests
            serializer.fields['date'].required = False
            serializer.fields['customer_name'].required = False
       
        return serializer

    def create(self, request, *args, **kwargs):
        """
        Create a new Invoice along with its details.
        """
        details_data = request.data.pop('details', [])
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, details_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, details_data):
        """
        Perform creation of Invoice and associated details.
        """
        invoice = serializer.save()
        for detail_data in details_data:
            detail_serializer = InvoiceDetailSerializer(data=detail_data)
            detail_serializer.is_valid(raise_exception=True)
            detail_serializer.save(invoice=invoice)
                # Collect validation errors for each detail instance

    def update(self, request, *args, **kwargs):
        """
        Update an existing Invoice along with its details.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        """
        Perform update of Invoice and associated details.
        """
        instance = serializer.instance
        print(instance.date, instance.customer_name)
        data = self.request.data
        
        # Update customer name if provided
        customer_name = data.get('customer_name')
        if customer_name is not None:
            instance.customer_name = customer_name
        
        # Update date if provided
        date = data.get('date')
        if date is not None:
            instance.date = date
        
        details_data = data.get('details', [])
        
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            
            if detail_id:
                try:
                    detail_instance = InvoiceDetail.objects.get(id=detail_id, invoice=instance)
                    detail_serializer = InvoiceDetailSerializer(detail_instance, data=detail_data, partial=True)
                    detail_serializer.is_valid(raise_exception=True)
                    detail_serializer.save()
                except InvoiceDetail.DoesNotExist:
                    raise exceptions.NotFound(detail_id)  # Handle if InvoiceDetail does not exist
            else:
                # Create new detail
                InvoiceDetail.objects.create(invoice=instance, **detail_data)
        
        instance.save()