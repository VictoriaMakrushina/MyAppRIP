# Generated by Django 2.0 on 2017-12-20 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Название курса')),
                ('description', models.TextField(verbose_name='Описание курса')),
                ('cost', models.IntegerField(verbose_name='Стоимость курса')),
                ('avatar', models.ImageField(default='course_images/no-avatar1.jpg', upload_to='course_images/')),
            ],
            options={
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='Repetitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='ФИО репетитора')),
                ('рhone_nomber', models.CharField(max_length=20, verbose_name='Телефон')),
                ('description', models.TextField(verbose_name='Личная информация')),
                ('avatar', models.ImageField(default='rep_images/no-avatar1.jpg', upload_to='rep_images/')),
            ],
            options={
                'db_table': 'repetitors',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='repetitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Repetitor', verbose_name='Автор'),
        ),
    ]