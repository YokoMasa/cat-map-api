import json
from decimal import Decimal

from django.test import TestCase, Client

from .models import Cat, Area
from user.models import User

class CatTest(TestCase):

  def test_cat_to_dict(self):
    user = User(
      name="john", 
      email="aaaaaaa@gmail.com", 
      password_digest="sdfasdf", 
      token="ddfsdfs",
      login_type="NM",
    )
    user.save()
    area = Area(code="15555")
    cat = Cat(name="shiro", longitude=1.5, latitude=14.223, area=area, user=user)
    cat_dict = cat.to_dict()
    self.assertEqual(cat_dict["name"], "shiro")
    self.assertEqual(cat_dict["longitude"], Decimal("1.5"))
    self.assertEqual(cat_dict["area"]["code"], "15555")

class CatViewTest(TestCase):

  @classmethod
  def setUpTestData(cls):
    user = User(
      name="john", 
      email="aaaaaaa@gmail.com", 
      password_digest="sdfasdf", 
      token="ddfsdfs",
      login_type="NM",
    )
    user.save()
    cls.area1 = Area.objects.create(code=111111)
    cls.area2 = Area.objects.create(code=222222)
    cls.cat1 = Cat.objects.create(name="cat1", longitude=22.22, latitude=22.22, area=cls.area1, user=user)
    cls.cat2 = Cat.objects.create(name="cat2", longitude=33.33, latitude=33.33, area=cls.area1, user=user)
    cls.cat3 = Cat.objects.create(name="cat3", longitude=44.44, latitude=44.44, area=cls.area2, user=user)
  
  def setUp(self):
    self.client = Client()

  def test_blank_query(self):
    response = self.client.get("/cat/list/")
    self.assertEqual(response.status_code, 200)

  def test_multiple_cats_in_one_area(self):
    response = self.client.get("/cat/list/?area=111111")
    obj = json.loads(response.content)
    self.assertEqual(len(obj), 2)
  
  def test_cats_in_multiple_areas(self):
    response = self.client.get("/cat/list/?area=111111&area=222222")
    obj = json.loads(response.content)
    self.assertEqual(len(obj), 3)
  
  def test_unknown_area(self):
    response = self.client.get("/cat/list/?area=333333")
    obj = json.loads(response.content)
    self.assertEqual(len(obj), 0)
    