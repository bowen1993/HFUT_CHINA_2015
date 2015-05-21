from django.db import models
import datetime

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=64)
    email = models.EmailField()
    is_confirmed = models.BooleanField()


    def __unicode__(self):
        return self.username

    class Meta:
        db_table="bio_user"


class UserSafety(models.Model):
    user = models.ForeignKey(User)
    activation_key = models.CharField(max_length=64, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __unicode__(self):
        return self.user.username

    class Meta:
        db_table = 'bio_usersafety'