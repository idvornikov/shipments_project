import uuid

from django.db import models


class Shipment(models.Model):
    track_number = models.UUIDField(help_text="Tracking number", default=uuid.uuid4)
    description = models.TextField(help_text="Shipment description", blank=True, default="")
    sender_address = models.TextField(help_text="Sender address")
    recipient_address = models.TextField(help_text="Recipient address")
    date_sent = models.DateTimeField(help_text="Parcel send date")
    date_delivered = models.DateTimeField(help_text="Parcel delivery date", default=None, null=True, blank=True)
    weight = models.FloatField(help_text="Parcel weight in kilograms")

    class Meta:
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        ordering = ["-date_sent"]
        indexes = [models.Index(fields=["track_number"])]

    def __str__(self):
        return str(self.track_number)
