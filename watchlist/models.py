from django.db import models

# Create your models here.


class Movie(models.Model):
    """A movie to watch."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)
    year = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.year})"