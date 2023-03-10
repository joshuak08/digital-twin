from django.db import models


# Each Post has parameters.
# Create your models here.
class Document(models.Model):
    elemID = models.IntegerField(db_column='elemID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)

    class Meta:
        managed = False

class SimDataTable(models.Model):
    # elemID = models.IntegerField(db_column='elemID', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    # name = models.TextField(blank=True, null=True)
    # params = models.TextField(blank=True, null=True)
    components = models.TextField(db_column='components', blank=True, null=False, primary_key=True)
    snapshots = models.IntegerField(blank=True, null=True)
    waterLevel = models.IntegerField(blank=True, null=True)
    sanddisp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        constraints = [
            models.UniqueConstraint(
                fields=['components', 'snapshots'], name='component_snapshot_primary_key'
            )
        ]
