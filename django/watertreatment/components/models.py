from django.db import models


# Each Post has parameters.
# Create your models here.
class Post(models.Model):
    name = models.CharField(max_length=100)
    elementID = models.IntegerField()
    content = models.TextField()
    params = models.JSONField()

    # Return post name when querying using SQL
    def __str__(self):
        return self.name
