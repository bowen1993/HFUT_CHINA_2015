from django.db import models
from accounts.models import User

# Create your models here.
# 

class parts(models.Model):
    part_id          = models.IntegerField(primary_key=True)
    ok               = models.BooleanField()
    part_name        = models.CharField(max_length=255)
    short_desc       = models.CharField(max_length=255)
    description      = models.TextField()
    part_type        = models.CharField(max_length=20)
    author           = models.CharField(max_length=200)
    status           = models.CharField(max_length=20)
    dominant         = models.BooleanField()
    discontinued     = models.IntegerField()
    part_status      = models.CharField(max_length=40)
    sample_status    = models.CharField(max_length=40)
    p_status_cache   = models.CharField(max_length=1000)
    s_status_cache   = models.CharField(max_length=1000)
    in_stock         = models.BooleanField()
    results          = models.CharField(max_length=20)
    favorite         = models.IntegerField()
    specified_u_list = models.TextField()
    deep_u_list      = models.TextField()
    deep_count       = models.IntegerField()
    ps_string        = models.TextField()
    scars            = models.CharField(max_length=20)
    barcode          = models.CharField(max_length=50)
    notes            = models.TextField()
    source           = models.TextField()
    nickname         = models.CharField(max_length=50)
    premium          = models.IntegerField()
    categories       = models.CharField(max_length=500)
    sequence         = models.TextField()
    sequence_length  = models.IntegerField()

    def __unicode__(self):
        return self.part_name

    class Meta:
        db_table = 'bio_parts' 

class functions(models.Model):
    function_id = models.IntegerField(primary_key=True)
    function    = models.CharField(max_length=128)

    def __unicode__(self):
        return self.function

    class Meta:
        db_table = 'bio_functions'


class tracks(models.Model):
    track    = models.CharField(max_length=64)

    def __unicode__(self):
        return self.track

    class Meta:
        db_table = 'bio_tracks'

class teams(models.Model):
    name = models.CharField(max_length=64)
    function = models.ForeignKey(functions)
    track = models.ForeignKey(tracks)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bio_team'

class project(models.Model):
    project_name = models.CharField(max_length=64)
    creator      = models.ForeignKey(User)
    create_time  = models.DateTimeField(auto_now_add=True)
    chain        = models.CharField(max_length=255, null=True)
    function     = models.ForeignKey(functions)
    track        = models.ForeignKey(tracks)
    is_deleted   = models.BooleanField(default=False)

    def __unicode__(self):
        return self.project_name

    class Meta:
        db_table = 'bio_project'

class team_parts(models.Model):
    team   = models.ForeignKey(teams)
    part = models.ForeignKey(parts)

    def __unicode__(self):
        return self.team_name

    class Meta:
        db_table = 'bio_team_parts'


class user_project(models.Model):
    user    = models.ForeignKey(User)
    project = models.ForeignKey(project)

    def __unicode__(self):
        return self.user

    class Meta:
        db_table = 'bio_user_project'



