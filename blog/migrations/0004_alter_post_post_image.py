# Generated by Django 4.1.7 on 2023-03-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, default='images/posts/default.jpg', upload_to='images/posts'),
        ),
    ]
