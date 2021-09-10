# Generated by Django 3.1.2 on 2021-07-03 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TypeFeedBack',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=254)),
                ('message', models.CharField(default='', max_length=255)),
                ('type_feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userpart.typefeedback')),
            ],
        ),
    ]