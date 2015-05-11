from django.db import models
from accounts.models import User

# Create your models here.

class Project(models.Model):
    project_name = models.CharField(max_length=64)
    creator = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)
    chain = models.CharField(max_length=255)
    function = models.CharField(max_length=64)
    track = models.CharField(max_length=64)
    is_deleted = models.BooleanField(default=False)

class user_project(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

class parts(models.Model):
    part_id = models.IntegerField(primary_key=True)
    ok = models.BooleanField()
    part_name = models.CharField(max_length=255)
    short_desc = models.CharField(max_length=100)
    description = models.TextField()
    part_type = models.CharField(max_length=20)
    author = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    dominant = models.BooleanField()
    discontinued = models.IntegerField()
    part_status = models.CharField(max_length=40)
    sample_status = models.CharField(max_length=40)
    p_status_cache = models.CharField(max_length=1000)
    s_status_cache = models.CharField(max_length=1000)
    creation_date = models.DateField(auto_now_add=False)
    m_datetime = models.DateTimeField(auto_now_add=False)
    in_stock = models.BooleanField()
    results = models.CharField(max_length=20)
    favorite = models.IntegerField()
    specified_u_list = models.TextField()
    deep_u_list = models.TextField()
    deep_count = models.IntegerField()
    ps_string = models.TextField()
    scars = models.CharField(max_length=20)
    barcode = models.CharField(max_length=50)
    notes = models.TextField()
    source = models.TextField()
    nickname = models.CharField(max_length=10)
    premium = models.IntegerField()
    categories = models.CharField(max_length=500)
    sequence = models.TextField()
    seq_edit_cache = models.TextField()
    sequence_length = models.IntegerField()
    