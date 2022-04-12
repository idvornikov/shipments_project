from django.db import migrations
from faker import Faker
from pytz import UTC

fake = Faker()


def create_dummy_data(apps, schema_editor):
    for _ in range(17):
        shipment = apps.get_model("shipments", "Shipment")
        shipment.objects.create(
            description=fake.first_name(),
            sender_address=fake.address(),
            recipient_address=fake.address(),
            date_sent=fake.date_time(tzinfo=UTC),
            weight=1,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("shipments", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_dummy_data),
    ]
