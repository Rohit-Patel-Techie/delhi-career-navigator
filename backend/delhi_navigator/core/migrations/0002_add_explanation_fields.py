# Generated manually for API enhancements

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerrecommendation',
            name='why_recommended',
            field=models.TextField(blank=True, help_text='Clear explanation of why this pathway fits the user'),
        ),
        migrations.AddField(
            model_name='careerrecommendation',
            name='considerations',
            field=models.TextField(blank=True, help_text='Trade-offs, challenges, or important considerations'),
        ),
        migrations.AddField(
            model_name='careerrecommendation',
            name='fit_score',
            field=models.CharField(blank=True, help_text="Qualitative fit assessment (e.g., 'Strong fit', 'Worth exploring')", max_length=50),
        ),
    ]
