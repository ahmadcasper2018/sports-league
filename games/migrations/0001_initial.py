# Generated by Django 4.2 on 2023-06-03 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_one', models.PositiveIntegerField()),
                ('score_two', models.PositiveIntegerField()),
                ('team_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_one', to='games.team')),
                ('team_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_two', to='games.team')),
            ],
        ),
    ]
