from django.contrib import admin

from .models import Questions, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionsAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    list_display = ['question_text', 'pub_date', 'was_published_recently']

    fieldsets = [
        ('Soru bilgileri', {'fields': ['question_text']}),
        ('Tarih bilgileri', {'fields': ['pub_date'], 'classes': ['collapse']})
    ]

    search_fields = ['question_text']

    inlines = [ChoiceInline]

admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Choice)