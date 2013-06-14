from django.db import models
from django.contrib.auth.models import User

class SurveyPaper(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User)
    description = models.TextField()
    pub_date = models.DateTimeField('Date published', auto_now_add=True)

    def __unicode__(self):
        return self.title

class Question(models.Model):
    surveypaper = models.ForeignKey(SurveyPaper)
    content = models.CharField('Question Text', max_length=200)

    def __unicode__(self):
        return self.content

class Choice(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField('Choice Text', max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.content
