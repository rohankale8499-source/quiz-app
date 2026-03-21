from django.contrib import admin
from .models import Category, Question, Choice, Result


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result)
