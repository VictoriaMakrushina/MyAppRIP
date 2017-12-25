from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
from  django.forms  import  ModelForm
from django.contrib.auth.models import User
from .models import Course, Repetitor
from .views import *


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserRegistrationForm(forms.Form):
    login = forms.CharField(label='Логин номер телефона',min_length=5)
    password = forms.CharField(
       label='Пароль',
       min_length=8,
       widget=forms.PasswordInput
    )
    repeat_password = forms.CharField(
       label='Повторите пароль',
       widget=forms.PasswordInput
    )
    name = forms.CharField(label='ФИО')
    description = forms.CharField(label='Деятельность и достижения:')
    avatar = forms.ImageField(required=False)


    def clean_login(self):
        user_model = get_user_model()
        login = self.cleaned_data['login']
        if user_model.objects.filter(username=login):
            raise ValidationError('Этот телефон уже зарегестрирован')
        return login


    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        if self.cleaned_data.get('password') and self.cleaned_data.get('repeat_password'):
            if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
                raise ValidationError('Пароли не совпадают')
        return cleaned_data['password']

    def save(self):
        user_model = get_user_model()
        ava_pic = self.cleaned_data['avatar']
        if not ava_pic:
            ava_pic = 'rep_images/no-avatar1.jpg'
        user = user_model.objects.create_user(
           username=self.cleaned_data['login'],
           password=self.cleaned_data['password'],
           name=self.cleaned_data['name'],
           description=self.cleaned_data['description'],
           avatar=ava_pic,

        )
        return user

class NewCourse(forms.Form):
    name = forms.CharField(label = 'Название курса')
    description = forms.CharField(label='Описание курса:')
    cost = forms.IntegerField(label='Стоимость:')
    avatar = forms.ImageField(required=False)
    repetitor_id = Repetitor.is_active


    def save(self):
        course = CourseView.get(self, request, id(self))
        ava_pic = self['avatar']
        if not ava_pic:
            ava_pic = 'rep_images/no-avatar1.jpg'
        course = Course(
            name=self['name'],
            description=self['description'],
            cost=self['cost'],
            # repetitor=self.repetitor.is_active,
            avatar=ava_pic,
        )
        return course

class  CourseForm ( ModelForm ):

    # description = forms.CharField(
    #     widget=forms.Textarea,
    #     label='Описание'
    # )
    class  Meta :
         model  =  Course
         fields  =  [ 'name' ,  'description' ,  'cost' ,  'repetitor', 'avatar' ]
         exclude = ('user_posted',)