from django.db import models
from user.models import User

class Area(models.Model):
  code = models.CharField(max_length=50, unique=True)

  def to_dict(self):
    return {
      "id": self.id,
      "code": self.code,
    }

  def __str__(self):
    return self.code

class Cat(models.Model):
  name = models.CharField(max_length=60)
  latitude = models.DecimalField(max_digits=9, decimal_places=6)
  longitude = models.DecimalField(max_digits=9, decimal_places=6)
  area = models.ForeignKey("Area", on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  def to_dict(self):
    return {
      "id": self.id,
      "name": self.name,
      "latitude": float(self.latitude),
      "longitude": float(self.longitude),
      "area": self.area.to_dict(),
      "images": self._images_list(),
      "parent": self.user.name,
    }
  
  def _images_list(self):
    existing_images = \
      filter(lambda image: image.file_actually_exists(), self.catimage_set.all())
    return list(map(lambda image: image.to_dict(), existing_images))

  def __str__(self):
    return self.name

class CatImage(models.Model):
  cat = models.ForeignKey("Cat", on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  raw_image = models.ImageField(upload_to="cats/")
  thumbnail = models.ImageField(upload_to="cats/")

  def file_actually_exists(self):
    return self.raw_image and self.thumbnail

  def to_dict(self):
    return {
      "id": self.id,
      "raw_image": self.raw_image.url,
      "thumbnail": self.thumbnail.url,
    }

  def __str__(self):
    return self.cat.name

class CatComment(models.Model):
  comment = models.CharField(max_length=255)
  cat = models.ForeignKey("Cat", on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)

  def to_dict(self):
    return {
      "id": self.id,
      "user": self.user.name,
      "created_at": self.created_at,
      "comment": self.comment
    }
