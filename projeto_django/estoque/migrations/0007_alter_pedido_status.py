# Generated by Django 5.1.1 on 2024-11-28 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_alter_material_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('em andamento', 'Em andamento'), ('concluido', 'Concluído')], default='pendente', max_length=20),
        ),
    ]
