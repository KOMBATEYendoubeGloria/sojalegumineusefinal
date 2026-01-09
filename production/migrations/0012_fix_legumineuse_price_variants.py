from django.db import migrations
import unicodedata


def normalize(name):
    if not name:
        return ''
    s = unicodedata.normalize('NFKD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.strip().lower()


def set_variant_prices(apps, schema_editor):
    Legumineuse = apps.get_model('production', 'Legumineuse')
    price_map = {
        'haricot': 2000,
        'arachide': 2500,
        'soja': 600,
        'sodja': 600,
        'niebe': 1500,
        'niebé': 1500,
        'niébé': 1500,
    }
    for leg in Legumineuse.objects.all():
        key = normalize(leg.nom)
        if key in price_map:
            leg.prix_unitaire = price_map[key]
            leg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0011_set_legumineuse_prices'),
    ]

    operations = [
        migrations.RunPython(set_variant_prices),
    ]
