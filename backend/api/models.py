from django.db import models

# Create your models here.
class Test(models.Model):
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uid = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'

class Sport(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sport'


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class HabsosT(models.Model):
    my_row_id = models.BigAutoField(primary_key=True)
    state_id = models.CharField(db_column='STATE_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=128, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.
    sample_date = models.CharField(db_column='SAMPLE_DATE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sample_depth = models.FloatField(db_column='SAMPLE_DEPTH', blank=True, null=True)  # Field name made lowercase.
    genus = models.CharField(db_column='GENUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    species = models.CharField(db_column='SPECIES', max_length=50, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cellcount = models.IntegerField(db_column='CELLCOUNT', blank=True, null=True)  # Field name made lowercase.
    cellcount_unit = models.CharField(db_column='CELLCOUNT_UNIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cellcount_qa = models.IntegerField(db_column='CELLCOUNT_QA', blank=True, null=True)  # Field name made lowercase.
    salinity = models.FloatField(db_column='SALINITY', blank=True, null=True)  # Field name made lowercase.
    salinity_unit = models.CharField(db_column='SALINITY_UNIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    salinity_qa = models.IntegerField(db_column='SALINITY_QA', blank=True, null=True)  # Field name made lowercase.
    water_temp = models.IntegerField(db_column='WATER_TEMP', blank=True, null=True)  # Field name made lowercase.
    water_temp_unit = models.CharField(db_column='WATER_TEMP_UNIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    water_temp_qa = models.IntegerField(db_column='WATER_TEMP_QA', blank=True, null=True)  # Field name made lowercase.
    wind_dir = models.IntegerField(db_column='WIND_DIR', blank=True, null=True)  # Field name made lowercase.
    wind_dir_unit = models.CharField(db_column='WIND_DIR_UNIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wind_dir_qa = models.IntegerField(db_column='WIND_DIR_QA', blank=True, null=True)  # Field name made lowercase.
    wind_speed = models.IntegerField(db_column='WIND_SPEED', blank=True, null=True)  # Field name made lowercase.
    wind_speed_unit = models.CharField(db_column='WIND_SPEED_UNIT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    wind_speed_qa = models.IntegerField(db_column='WIND_SPEED_QA', blank=True, null=True)  # Field name made lowercase.
    sample_datetime = models.DateTimeField(db_column='SAMPLE_DATETIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'habsos_t'

class HabsosJ(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    state_id = models.CharField(db_column='STATE_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE')  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE')  # Field name made lowercase.
    sample_date = models.CharField(db_column='SAMPLE_DATE', max_length=45)  # Field name made lowercase.
    sample_depth = models.FloatField(db_column='SAMPLE_DEPTH', blank=True, null=True)  # Field name made lowercase.
    genus = models.CharField(db_column='GENUS', max_length=45, blank=True, null=True)  # Field name made lowercase.
    species = models.CharField(db_column='SPECIES', max_length=45, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(db_column='CATEGORY', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cellcount = models.IntegerField(db_column='CELLCOUNT')  # Field name made lowercase.
    cellcount_unit = models.CharField(db_column='CELLCOUNT_UNIT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cellcount_qa = models.IntegerField(db_column='CELLCOUNT_QA', blank=True, null=True)  # Field name made lowercase.
    salinity = models.FloatField(db_column='SALINITY', blank=True, null=True)  # Field name made lowercase.
    salinity_unit = models.CharField(db_column='SALINITY_UNIT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    salinity_qa = models.IntegerField(db_column='SALINITY_QA', blank=True, null=True)  # Field name made lowercase.
    water_temp = models.FloatField(db_column='WATER_TEMP', blank=True, null=True)  # Field name made lowercase.
    water_temp_unit = models.CharField(db_column='WATER_TEMP_UNIT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    water_temp_qa = models.IntegerField(db_column='WATER_TEMP_QA', blank=True, null=True)  # Field name made lowercase.
    wind_dir = models.FloatField(db_column='WIND_DIR', blank=True, null=True)  # Field name made lowercase.
    wind_dir_unit = models.CharField(db_column='WIND_DIR_UNIT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    wind_dir_qa = models.IntegerField(db_column='WIND_DIR_QA', blank=True, null=True)  # Field name made lowercase.
    wind_speed = models.FloatField(db_column='WIND_SPEED', blank=True, null=True)  # Field name made lowercase.
    wind_speed_unit = models.CharField(db_column='WIND_SPEED_UNIT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    wind_speed_qa = models.IntegerField(db_column='WIND_SPEED_QA', blank=True, null=True)  # Field name made lowercase.
    sample_datetime = models.DateTimeField(db_column='SAMPLE_DATETIME', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'habsos_j'


class HabsosPrediction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    state_id = models.CharField(db_column='STATE_ID', max_length=2, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=45, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE')  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE')  # Field name made lowercase.
    sample_date = models.CharField(db_column='SAMPLE_DATE', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sample_datetime = models.DateTimeField(db_column='SAMPLE_DATETIME', blank=True, null=True)  # Field name made lowercase.
    salinity = models.FloatField(db_column='SALINITY', blank=True, null=True)  # Field name made lowercase.
    water_temp = models.FloatField(db_column='WATER_TEMP', blank=True, null=True)  # Field name made lowercase.
    wind_dir = models.FloatField(db_column='WIND_DIR', blank=True, null=True)  # Field name made lowercase.
    wind_speed = models.FloatField(db_column='WIND_SPEED', blank=True, null=True)  # Field name made lowercase.
    predict_category = models.CharField(db_column='PREDICT_CATEGORY', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'habsos_prediction'