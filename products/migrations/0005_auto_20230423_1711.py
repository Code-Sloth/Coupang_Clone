# Generated by Django 3.2.18 on 2023-04-23 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('패션의류_잡화', '패션의류/잡화'), ('뷰티', '뷰티'), ('식품', '식품'), ('주방용품', '주방용품'), ('생활용품', '생활용품')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='star',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=5),
        ),
    ]
