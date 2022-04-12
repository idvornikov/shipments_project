from http import HTTPStatus

from rest_framework.test import APITestCase
from .factories import ShipmentFactory
from ..models import Shipment


class TestShipmentViewSet(APITestCase):
    """Shipment viewset test class"""

    shipments_count: int

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.shipments_count = 4
        cls.shipments = ShipmentFactory.create_batch(cls.shipments_count)
        cls.url = "/api/shipments/"

    def test_create_shipment_with_correct_data(self):
        data = {
            "description": "test description",
            "sender_address": "sender address",
            "recipient_address": "recipient address",
            "date_sent": "2022-12-11 13:53:20",
            "weight": 1.33,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_create_shipment_with_wrong_data(self):
        data = {
            "description": "test description",
            "sender_address": "sender address",
            "recipient_address": "recipient address",
            "date_sent": "2022-12-11 13:53:20",
            "weight": "wrong weight",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_get_all_shipments(self):
        response = self.client.get("/api/shipments/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["count"], self.shipments_count)

    def test_get_specific_shipment(self):
        expected_shipment = self.shipments[0]
        response = self.client.get(f"{self.url}{expected_shipment.pk}/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        fetched_shipment = response.json()
        self.assertEqual(expected_shipment.weight, fetched_shipment["weight"])

    def test_partial_update_specific_shipment(self):
        updated_shipment = self.shipments[0]
        new_description = "new description"
        data = {"description": new_description}

        response = self.client.patch(f"{self.url}{updated_shipment.id}/", data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response_data = response.json()
        self.assertEqual(response_data["description"], new_description)
        shipment = Shipment.objects.get(id=updated_shipment.id)
        self.assertEqual(shipment.description, new_description)

    def test_delete_shipment(self):
        deleted_shipment = self.shipments[0]
        response = self.client.delete(f"{self.url}{deleted_shipment.id}/")
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        shipments_count = Shipment.objects.count()
        self.assertEqual(shipments_count, 3)
        self.assertFalse(Shipment.objects.filter(id=deleted_shipment.id).exists())
