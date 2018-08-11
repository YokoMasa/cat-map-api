import json

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from PIL import Image

from user.models import User 
from user.decorators import require_login
from shared import errors
from cat.models import Area, Cat, CatImage
from cat.forms import CatForm, CatImageForm, CatCommentForm
from . import image_handler

@require_http_methods(["GET"])
def get(request, id):
  try:
    cat = Cat.objects.get(pk=id)
    cat_json = json.dumps(cat.to_dict(), ensure_ascii=False, indent=2)
    return HttpResponse(cat_json)
  except ObjectDoesNotExist:
    return HttpResponse(errors.NOT_FOUND, status=404)

@require_http_methods(["GET"])
def getlist(request):
  area_codes = request.GET.getlist("area")
  cats = Cat.objects.select_related("area").prefetch_related("catimage_set").filter(area__code__in=area_codes)
  cats_data = list(map(lambda cat: cat.to_dict(), cats))
  cats_json = json.dumps(cats_data, ensure_ascii=False, indent=2)
  return HttpResponse(cats_json)

@require_login
@require_http_methods(["POST"])
def create(request, user):
  form = CatForm(request.POST, request.FILES)
  if form.is_valid():
    area = _get_area(form.cleaned_data["area_code"])
    cat = Cat(
      name = form.cleaned_data["name"],
      longitude = form.cleaned_data["longitude"],
      latitude = form.cleaned_data["latitude"],
      user = user,
      area = area
    )
    cat.save()
    image_handler.save_cat_image(cat, user, form.cleaned_data["cat_image"])
    return HttpResponse()
  else:
    return HttpResponse(errors.INSUFFICIENT_PARAMS, status=400)

@require_login
@require_http_methods(["POST"])
def create_image(request, user, id):
  form = CatImageForm(request.POST, request.FILES)
  if form.is_valid():
    try:
      cat = Cat.objects.get(pk=id)
      image_handler.save_cat_image(cat, user, form.cleaned_data["cat_image"])
      return HttpResponse(status=200)
    except ObjectDoesNotExist:
      return HttpResponse(errors.NOT_FOUND, status=404)
  else:
    return HttpResponse(errors.INSUFFICIENT_PARAMS, status=400)

def _get_area(area_code):
  try:
    area = Area.objects.get(code=area_code)
    return area
  except ObjectDoesNotExist:
    area = Area(code=area_code)
    area.save()
    return area
