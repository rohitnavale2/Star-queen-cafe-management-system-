from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0003_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='gallery/'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image_url',
            field=models.URLField(blank=True, help_text='Optional: use URL if not uploading a file'),
        ),
        migrations.AlterModelOptions(
            name='galleryimage',
            options={'ordering': ['-created_at']},
        ),
    ]
