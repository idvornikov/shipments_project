from rest_framework import serializers

from ..models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = [
            "id",
            "track_number",
            "description",
            "sender_address",
            "recipient_address",
            "date_sent",
            "date_delivered",
            "weight",
        ]

        extra_kwargs = {"date_delivered": {"required": False}, "track_number": {"required": False}}
