from django.db import models

class Poll(models.Model):
    name = models.CharField(max_length = 64)
    options = models.IntegerField()
    def __str__(self):
        return self.name