from django.contrib import admin
from survey.models import SurveyPaper, Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class SurveyPaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')

admin.site.register(SurveyPaper, SurveyPaperAdmin)
admin.site.register(Question, QuestionAdmin)
