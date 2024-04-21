# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_question'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ForecastJ(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='DATETIME')  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE')  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE')  # Field name made lowercase.
    water_temp = models.FloatField(db_column='WATER_TEMP', blank=True, null=True)  # Field name made lowercase.
    salinity = models.FloatField(db_column='SALINITY', blank=True, null=True)  # Field name made lowercase.
    wind_speed = models.FloatField(db_column='WIND_SPEED', blank=True, null=True)  # Field name made lowercase.
    wind_dir = models.IntegerField(db_column='WIND_DIR', blank=True, null=True)  # Field name made lowercase.
    predict_category = models.CharField(db_column='PREDICT_CATEGORY', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forecast_j'


class ForecastJTest(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    datetime = models.DateTimeField(db_column='DATETIME')  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE')  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE')  # Field name made lowercase.
    water_temp = models.FloatField(db_column='WATER_TEMP', blank=True, null=True)  # Field name made lowercase.
    salinity = models.FloatField(db_column='SALINITY', blank=True, null=True)  # Field name made lowercase.
    wind_speed = models.FloatField(db_column='WIND_SPEED', blank=True, null=True)  # Field name made lowercase.
    wind_dir = models.IntegerField(db_column='WIND_DIR', blank=True, null=True)  # Field name made lowercase.
    predict_category = models.CharField(db_column='PREDICT_CATEGORY', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'forecast_j_test'


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


class HabsosJLat0P2(models.Model):
    id = models.IntegerField(db_column='ID')  # Field name made lowercase.
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
        db_table = 'habsos_j_lat0p2'


class HabsosJTest(models.Model):
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
        db_table = 'habsos_j_test'


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


class HabsosT(models.Model):
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


class Sport(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sport'


class Test(models.Model):
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    uid = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
