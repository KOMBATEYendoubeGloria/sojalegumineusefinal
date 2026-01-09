from django.db import migrations


def set_prices(apps, schema_editor):
    Legumineuse = apps.get_model('production', 'Legumineuse')
    price_map = {
        'haricot': 2000,
        'arachide': 2500,
        'soja': 600,
        'niébé': 1500,
    }
    for leg in Legumineuse.objects.all():
        name = (leg.nom or '').strip().lower()
        if name in price_map:
            leg.prix_unitaire = price_map[name]
            leg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0010_legumineuse_prix_unitaire'),
    ]

    operations = [
        migrations.RunPython(set_prices),
    ]
