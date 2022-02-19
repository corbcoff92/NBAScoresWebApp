# Generated by Django 4.0.2 on 2022-02-14 09:22

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
                ('team_name', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=30)),
                ('abbreviation', models.CharField(max_length=3)),
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.IntegerField()),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='NBA.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='NBA.team')),
            ],
        ),
    ]