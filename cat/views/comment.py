import json
from datetime import datetime

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

@require_http_methods(["GET"])
def get(request, id):
  try:
    cat = Cat.objects.prefetch_related("catcomment_set").get(pk=id)
    comments = list(map(lambda comment: comment.to_dict(), cat.catcomment_set.order_by("-created_at").all()))
    data = json.dumps(comments, ensure_ascii=False, indent=2, default=_support_datetime)
    return HttpResponse(data)
  except ObjectDoesNotExist:
    return HttpResponse(errors.NOT_FOUND, status=404)

@require_login
@require_http_methods(["POST"])
def create(request, user, id):
  form = CatCommentForm(request.POST)
  if form.is_valid():
    try:
      cat = Cat.objects.get(pk=id)
      user.catcomment_set.create(
        comment=form.cleaned_data["comment"],
        cat=cat
      )
      return HttpResponse(status=200)
    except ObjectDoesNotExist:
      return HttpResponse(errors.NOT_FOUND, status=404)
  else:
    return HttpResponse(errors.INSUFFICIENT_PARAMS, status=400)

def _support_datetime(o):
  if isinstance(o, datetime):
    return o.isoformat()
  raise TypeError(repr(o) + " is not JSON serializable")