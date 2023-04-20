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
    id = models.TextField(db_column='id', blank=True, null=False, primary_key=True)
    snap_num = models.IntegerField(blank=True, null=True)
    water_vol = models.IntegerField(blank=True, null=True)
    particulate = models.IntegerField(blank=True, null=True)
    backwash = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        constraints = [
            models.UniqueConstraint(
                fields=['components', 'snapshots'], name='component_snapshot_primary_key'
            )
        ]
