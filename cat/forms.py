from django import forms

class CatForm(forms.Form):
  name = forms.CharField(max_length=50)
  latitude = forms.DecimalField(
    min_value=-90,
    max_value=90,
  )
  longitude = forms.DecimalField(
    min_value=-180,
    max_value=180,
  )
  area_code = forms.CharField(max_length=30)
  cat_image = forms.ImageField()

class CatImageForm(forms.Form):
  cat_image = forms.ImageField()

class CatCommentForm(forms.Form):
  comment = forms.CharField(max_length=255)