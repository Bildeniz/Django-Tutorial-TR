import datetime

from django.db import models
from django.utils import timezone

from django.contrib import admin

class Questions(models.Model):
    question_text = models.CharField("Soru metni", max_length=200)
    pub_date = models.DateTimeField("Yayın tarihi")

    def __str__(self) -> str:
        return self.question_text
    
    @admin.display(
            boolean=True,
            ordering=pub_date,
            description='Yeni mi yayınlandı')
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    class Meta:
        verbose_name = 'Soru'
        verbose_name_plural = 'Sorular'


class Choice(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.choice_text

    class Meta:
        verbose_name = 'Seçenek'
        verbose_name_plural = 'Seçenekler'
