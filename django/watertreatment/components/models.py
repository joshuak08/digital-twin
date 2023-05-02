from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

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

# All the attributes to run the simulation
# class SimInput(models.Model):
#     # def validate_interval(value):
#     #     if value < 0.0 or value > 11000000.0:
#     #         print('test')
#     #         raise ValidationError(_('%(value)s must be in the range [0.0, 1.0]'), params={'value': value})
#     # Want to try to create 4 different fields and merge them all into 1 list for particulates in each tank
#     # no more than 11M
#     tank0 = models.FloatField('Amount of pre-existing particulate in tank 1 [Max value: 11000000] (mg)', blank=True,
#                               default=0, validators=[MinValueValidator(0, message="Please enter a valid value asdf."), MaxValueValidator(11000000, message="Please enter a valid value asdf.")])
#     tank1 = models.FloatField('Amount of pre-existing particulate in tank 2 [Max value: 112000000] (mg)', blank=True,
#                               default=0, validators=[MinValueValidator(0, message="Please enter a valid value asdf."), MaxValueValidator(11000000, message="Please enter a valid value asdf.")])
#     tank2 = models.FloatField('Amount of pre-existing particulate in tank 3 [Max value: 11000000] (mg)', blank=True,
#                               default=0, validators=[MinValueValidator(0), MaxValueValidator(11000000)])
#     tank3 = models.FloatField('Amount of pre-existing particulate in tank 4 [Max value: 11000000] (mg)', blank=True,
#                               default=0, validators=[MinValueValidator(0), MaxValueValidator(11000000)])
#     # no more than 0.5
#     average_flow = models.FloatField('Average Flow (m^3/s)', validators=[MinValueValidator(0), MaxValueValidator(1)])
#     average_tss = models.FloatField('Amount of particulate in waste water (mg/l)')
#     sim_length = models.PositiveIntegerField('Length of time for simulation (s)', error_messages={
#         'invalid': "adsfasdfasdfasdfasdf asdf."
#     })
#     # If checked data will be displayed as 'on'/'off' instead of true or false
#     testing = models.BooleanField('Is this part of testing?')
#     class Meta:
#         managed = False

# class MinMaxFloat(models.FloatField):
#     def __init__(self, min_value=None, max_value=None, *args, **kwargs):
#         self.min_value, self.max_value = min_value, max_value
#         super(MinMaxFloat, self).__init__(*args, **kwargs)
#
#     def formfield(self, **kwargs):
#         defaults = {'min_value': self.min_value, 'max_value' : self.max_value}
#         defaults.update(kwargs)
#         return super(MinMaxFloat, self).formfield(**defaults)