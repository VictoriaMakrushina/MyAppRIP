from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from polls.models import *


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ['name']
    search_fields = ('id', 'name')

admin.site.register(Course, CourseAdmin)


class CooperateInline(admin.TabularInline):
    model = Repetitor.cooperate.through
    fk_name = 'from_repetitor'


class RepetitorAdmin(UserAdmin):
    inlines = (CooperateInline,)
    exclude = ['cooperated']
    pass

admin.site.register(Repetitor, RepetitorAdmin)

