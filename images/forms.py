from django import forms
from urllib.request import urlopen,Request
from django.core.files.base import ContentFile
from .models import Image
from django.utils.text import slugify

class ImageCreatForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','desc')
        widgets = {
            'url':forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("You must provide only '.jpg' or '.jpeg' extensions")
        return url

    def save(self,commit=True,*args,**kwargs):
        image = super(ImageCreatForm,self).save(commit=False)
        image_url = self.cleaned_data.get('url')
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())

        req = Request(image_url,headers={'User-Agent':'Mozilla/5.0'})
        response = urlopen(req).read()
        image.image.save(image_name,ContentFile(response),save=False)

        if commit:
            image.save()
        return image
