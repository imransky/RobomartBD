# Generated by Django 4.2.2 on 2023-09-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Basic_Api', '0028_product_product_discription_product_product_tutorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='catagorys',
            field=models.ManyToManyField(blank=True, null=True, to='Basic_Api.catagory'),
        ),
    ]
