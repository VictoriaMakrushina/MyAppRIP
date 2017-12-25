from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Repetitor(AbstractUser):
    class Meta:
        db_table = "repetitors"
    name = models.CharField(max_length=30, verbose_name='ФИО репетитора')
    рhone_nomber = models.CharField(max_length=20, verbose_name='Телефон')
    description=models.TextField(verbose_name='Личная информация')
    avatar = models.ImageField(
        upload_to='rep_images/',
        default='rep_images/no-avatar1.jpg'
    )
    cooperate = models.ManyToManyField(
        'self',
        related_name='cooperated',
        symmetrical=False
    )
    # cooperate = models.ManyToManyField(
    #    'self',
    #    related_name='cooperate',
    #    symmetrical=False
    # )
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('repet-detail', kwargs={'id': self.pk})

class Course(models.Model):
    class Meta:
        db_table = "courses"
    name = models.CharField(max_length=30, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса')
    cost = models.IntegerField(verbose_name='Стоимость курса')
    repetitor = models.ForeignKey(
         settings.AUTH_USER_MODEL,
         on_delete = models.CASCADE,
         verbose_name = 'Автор'
    )
    avatar = models.ImageField(
        upload_to='course_images/',
        default='course_images/no-avatar1.jpg'
    )
    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('course-detail', kwargs={'pk': self.pk})




