from django.db import models
from django.conf import settings
from PIL import Image
from django.contrib.auth.models import User
# from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/',default='person.png')
    dob   = models.DateField(blank=True,null=True)

    def __str__(self):
        return '{} Profile'.format(self.user.username)

    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.width>300 or img.height>300:
            output_size= (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Contact(models.Model):
    user_from   = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rel_from_set')
    user_to     = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rel_to_set')
    created     = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,self.user_to)


User.add_to_class('following',models.ManyToManyField('self',through=Contact,related_name='followers',symmetrical=False))
