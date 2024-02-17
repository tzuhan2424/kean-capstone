from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uid = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'

class Sport(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sport'


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")