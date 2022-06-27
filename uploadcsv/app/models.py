from django.db import models

# Create your models here.
class Csv_file(models.Model):
    one = models.CharField(max_length = 250, null = True, blank = True)
    two = models.CharField(max_length = 250, null = True, blank = True)
    three = models.EmailField( blank=True, null=True)
    four = models.CharField(max_length = 250, null = True, blank = True)
    file_path = models.FileField(upload_to="Files", verbose_name="Files", blank=True, null=True)

    def __str__(self):
        return self.one
