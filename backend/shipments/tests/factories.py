import datetime

import factory.fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from ..models import Shipment


class ShipmentFactory(DjangoModelFactory):
    """Factory for creating Shipment model objects"""

    description = factory.fuzzy.FuzzyText()
    sender_address = factory.Faker("address")
    recipient_address = factory.Faker("address")
    date_sent = factory.fuzzy.FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=UTC))
    weight = factory.fuzzy.FuzzyFloat(0)

    class Meta:
        model = Shipment
