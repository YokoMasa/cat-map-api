from django.db import models

class User(models.Model):
  FACEBOOK = "FB"
  TWITTER = "TW"
  NORMAL = "NM"
  GOOGLE = "GG"
  LOGIN_TYPE_CHOICES = (
    (FACEBOOK, "Facebook"),
    (TWITTER, "Twitter"),
    (NORMAL, "Normal"),
    (GOOGLE, "Google"),
  )

  name = models.CharField(max_length=50)
  token = models.CharField(max_length=255, unique=True)
  login_type = models.CharField(max_length=2, choices=LOGIN_TYPE_CHOICES, default=NORMAL)
  sns_user_id = models.CharField(max_length=255, default="")

  def __str__(self):
    return self.name
