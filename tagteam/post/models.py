from django.db import models

# Create your models here.

class Post(models.Model):
    text = models.CharField(max_length=140)
    time_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

class Tag(models.Model):
    value = models.CharField(max_length=140, unique=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.value

class PostTag(models.Model):
    pid = models.ForeignKey(Post)
    tid = models.ForeignKey(Tag)

    def __unicode__(self):
        return "PID: {0}, TID: {1}".format(self.pid.id, self.tid.id)
