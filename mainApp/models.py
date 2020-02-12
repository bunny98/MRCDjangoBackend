from django.db import models

# Create your models here.
class FileTable(models.Model):
    file = models.FileField()
    filename = models.CharField(max_length=256, default="NOT SPECIFIED")

    def __str__(self):
        return self.filename