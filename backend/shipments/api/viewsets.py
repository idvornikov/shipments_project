from rest_framework import viewsets

from .serializers import ShipmentSerializer
from ..models import Shipment


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD operations with shipments.
    """
    queryset = Shipment.objects.all().order_by('-date_sent')
    serializer_class = ShipmentSerializer
