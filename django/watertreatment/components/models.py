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

class SimInput(models.Model):
    # average_flow, average_tss, sim_length, initial_particulates, testing
    average_flow = models.IntegerField('Average Flow')
    average_tss = models.IntegerField('Amount of particulate in waste water')
    sim_length = models.IntegerField('Length of time for simulation in seconds/minutes')
    # Want to try to create 4 different fields and merge them all into 1 list for particulates in each tank
    initial_particulates = models.IntegerField('Amount of pre-existing particulate in tanks')
    # If checked data will be displayed as 'on'/'off' instead of true or false
    testing = models.BooleanField('Is this part of testing?')
    class Meta:
        managed = False