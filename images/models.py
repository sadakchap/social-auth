from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Image(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='images_created')
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=255,blank=True)
    url         = models.URLField()
    image       = models.ImageField(upload_to='images/%Y/%m/%d/')
    desc        = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True,db_index=True)

    users_like  = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='images_liked',blank=True)

    total_likes = models.PositiveIntegerField(db_index=True,default=0)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super(Image,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('images:detail',kwargs={'id':self.pk,'slug':self.slug})
