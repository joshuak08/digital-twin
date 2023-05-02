from django.db import models
from django.core.validators import validate_comma_separated_integer_list

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
                fields=['id', 'snap_num'], name='component_snapshot_primary_key'
            )
        ]

class SimInput(models.Model):
    # Want to try to create 4 different fields and merge them all into 1 list for particulates in each tank
    # initial_particulates = models.IntegerField('Amount of pre-existing particulate in tanks', blank=True)
    tank0 = models.FloatField('Amount of pre-existing particulate in tank 1', blank=True, default=0)
    tank1 = models.FloatField('Amount of pre-existing particulate in tank 2', blank=True, default=0)
    tank2 = models.FloatField('Amount of pre-existing particulate in tank 3', blank=True, default=0)
    tank3 = models.FloatField('Amount of pre-existing particulate in tank 4', blank=True, default=0)
    # average_flow, average_tss, sim_length, initial_particulates, testing
    average_flow = models.FloatField('Average Flow')
    average_tss = models.FloatField('Amount of particulate in waste water')
    sim_length = models.IntegerField('Length of time for simulation in seconds')
    # If checked data will be displayed as 'on'/'off' instead of true or false
    testing = models.BooleanField('Is this part of testing?')
    class Meta:
        managed = False