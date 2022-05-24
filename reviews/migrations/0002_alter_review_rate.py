from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rate',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=2),
        ),
    ]
