# Generated by Django 4.2.2 on 2023-06-08 07:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('image', models.ImageField(default='customers/default.jpg', upload_to='customers/')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d{10}$|^\\d{11}$', "O número de telefone deve estar no formato: 'XXXXXXXXXX' ou 'XXXXXXXXXXX'", 'invalid')])),
                ('email', models.EmailField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title', verbose_name='slug')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status')),
                ('activate_date', models.DateTimeField(blank=True, help_text='keep empty for an immediate activation', null=True)),
                ('deactivate_date', models.DateTimeField(blank=True, help_text='keep empty for indefinite activation', null=True)),
                ('stock', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0.0)),
                ('image', models.ImageField(default='products/default.jpg', upload_to='products/')),
                ('commission_rate', models.FloatField(default=0.0)),
                ('cod_prod', models.CharField(blank=True, max_length=6, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('invoice_number', models.IntegerField(blank=True, null=True, unique=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lojinha.customer')),
            ],
            options={
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('image', models.ImageField(default='sellers/default.jpg', upload_to='sellers/')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^\\d{10}$|^\\d{11}$', "O número de telefone deve estar no formato: 'XX XXXX.XXXX' ou 'XX XXXXX.XXXX'", 'invalid')])),
                ('email', models.EmailField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Vendedor',
                'verbose_name_plural': 'Vendedores',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price_at_sale', models.FloatField()),
                ('discount', models.FloatField(default=0.0)),
                ('tax', models.FloatField(default=6.0)),
                ('commission', models.FloatField(default=0.0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lojinha.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='lojinha.order')),
            ],
            options={
                'verbose_name': 'Detalhe da Venda',
                'verbose_name_plural': 'Detalhes das Vendas',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lojinha.seller'),
        ),
        migrations.CreateModel(
            name='CommissionByDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(0, 'Segunda'), (1, 'Terça'), (2, 'Quarta'), (3, 'Quinta'), (4, 'Sexta'), (5, 'Sábado'), (6, 'Domingo')])),
                ('min_commission', models.FloatField()),
                ('max_commission', models.FloatField()),
            ],
            options={
                'unique_together': {('day_of_week',)},
            },
        ),
    ]
