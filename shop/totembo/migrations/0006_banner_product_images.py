# Banner mahsulotlariga rasmlar (static -> media, ImagesProduct)

import shutil
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.db import migrations


def copy_banner_images(apps, schema_editor):
    # Static rasmlar: shop/totembo/static/images/
    base = Path(settings.BASE_DIR)
    src_dir = base / 'totembo' / 'static' / 'images'
    if not src_dir.exists():
        return

    media_root = Path(settings.MEDIA_ROOT)
    products_dir = media_root / 'products'
    products_dir.mkdir(parents=True, exist_ok=True)

    Product = apps.get_model('totembo', 'Product')
    ImagesProduct = apps.get_model('totembo', 'ImagesProduct')

    mapping = [
        ('banner-mvmt-watch', 'hand-watch.png', 'banner_watch.png'),
        ('banner-everiot-bracelet', 'bracel.png', 'banner_bracelet.png'),
        ('banner-diadema-earring', 'serga.png', 'banner_earring.png'),
    ]

    for slug, src_name, dst_name in mapping:
        product = Product.objects.filter(slug=slug).first()
        if not product:
            continue
        if product.images.exists():
            continue
        src_path = src_dir / src_name
        if not src_path.exists():
            continue
        dst_path = products_dir / dst_name
        shutil.copy2(src_path, dst_path)
        rel_name = f'products/{dst_name}'
        with open(dst_path, 'rb') as f:
            ImagesProduct.objects.create(product=product, image=File(f, name=rel_name))


def remove_banner_images(apps, schema_editor):
    Product = apps.get_model('totembo', 'Product')
    ImagesProduct = apps.get_model('totembo', 'ImagesProduct')
    for slug in ['banner-mvmt-watch', 'banner-everiot-bracelet', 'banner-diadema-earring']:
        p = Product.objects.filter(slug=slug).first()
        if p:
            ImagesProduct.objects.filter(product=p).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('totembo', '0005_banner_products'),
    ]

    operations = [
        migrations.RunPython(copy_banner_images, remove_banner_images),
    ]
