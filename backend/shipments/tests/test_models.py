from django.test import TestCase

from ..models import Shipment
from .factories import ShipmentFactory


class TestShipmentModel(TestCase):
    def test_str_method(self):
        ShipmentFactory.create_batch(3)
        shipment = Shipment.objects.first()
        self.assertEqual(str(shipment.track_number), shipment.__str__())


