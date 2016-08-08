from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Url(models.Model):
    original_url = models.CharField(max_length=500, unique=True)
    shortened_url = models.CharField(max_length=100, unique=True)
    custom_url = models.CharField(max_length=100)
    visit_count = models.IntegerField()
    shorten_count = models.IntegerField()
    created_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.shortened_url