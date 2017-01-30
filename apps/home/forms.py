from django import forms

class ImageUploadForm(forms.Form):
    name = forms.CharField(max_length=255)
    image = forms.ImageField()
