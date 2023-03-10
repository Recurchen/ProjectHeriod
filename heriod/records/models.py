from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Record(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    period = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username