# Generated manually for banner products

from django.db import migrations


def create_banner_products(apps, schema_editor):
    Category = apps.get_model('totembo', 'Category')
    ModelProduct = apps.get_model('totembo', 'ModelProduct')
    Product = apps.get_model('totembo', 'Product')

    # Categories for banner (get or create)
    cat_watch, _ = Category.objects.get_or_create(
        slug='chasy',
        defaults={'title': 'Часы', 'parent': None}
    )
    cat_bracelet, _ = Category.objects.get_or_create(
        slug='braslety',
        defaults={'title': 'Браслеты', 'parent': None}
    )
    cat_earring, _ = Category.objects.get_or_create(
        slug='sergi',
        defaults={'title': 'Серьги', 'parent': None}
    )

    # Models (get or create)
    mod_watch, _ = ModelProduct.objects.get_or_create(
        slug='mvmt',
        defaults={'title': 'MVMT'}
    )
    mod_bracelet, _ = ModelProduct.objects.get_or_create(
        slug='everiot',
        defaults={'title': 'EVERIOT'}
    )
    mod_earring, _ = ModelProduct.objects.get_or_create(
        slug='diadema',
        defaults={'title': 'DIADEMA GRAND'}
    )

    # Banner products (get or create) — order: watch, bracelet, earring
    Product.objects.get_or_create(
        slug='banner-mvmt-watch',
        defaults={
            'title': 'Наручные часы MVMT',
            'desc': 'Стильные наручные часы с металлическим браслетом.',
            'price': 1128000,
            'quantity': 15,
            'color_name': 'Gold',
            'discount': 0,
            'category': cat_watch,
            'model': mod_watch,
        }
    )
    Product.objects.get_or_create(
        slug='banner-everiot-bracelet',
        defaults={
            'title': 'Браслет EVERIOT',
            'desc': 'Кожаный браслет с серебряными элементами.',
            'price': 150000,
            'quantity': 15,
            'color_name': 'Black',
            'discount': 0,
            'category': cat_bracelet,
            'model': mod_bracelet,
        }
    )
    Product.objects.get_or_create(
        slug='banner-diadema-earring',
        defaults={
            'title': 'Серьга DIADEMA GRAND',
            'desc': 'Элегантная серьга с фианитом.',
            'price': 95000,
            'quantity': 15,
            'color_name': 'Black',
            'discount': 0,
            'category': cat_earring,
            'model': mod_earring,
        }
    )


def remove_banner_products(apps, schema_editor):
    Product = apps.get_model('totembo', 'Product')
    Product.objects.filter(
        slug__in=['banner-mvmt-watch', 'banner-everiot-bracelet', 'banner-diadema-earring']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('totembo', '0004_emailsubscription_order_orderitem'),
    ]

    operations = [
        migrations.RunPython(create_banner_products, remove_banner_products),
    ]
