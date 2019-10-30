# Generated by Django 2.2.4 on 2019-10-30 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FactoryState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'factories_factory_states',
            },
        ),
        migrations.CreateModel(
            name='FactoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('base_production_rate', models.IntegerField(default=0)),
                ('build_cost', models.IntegerField(default=0)),
                ('base_upkeep_cost', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'factories_factory_types',
            },
        ),
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('level', models.IntegerField()),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=16)),
                ('is_for_sale', models.BooleanField(default=True)),
                ('price_per_unit', models.IntegerField(default=0)),
                ('production_rate', models.IntegerField(default=0)),
                ('units_stored', models.IntegerField(default=0)),
                ('upkeep_cost', models.IntegerField(default=0)),
                ('is_selling', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factories.FactoryState')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='factories.FactoryType')),
            ],
            options={
                'db_table': 'factories_factories',
            },
        ),
    ]
