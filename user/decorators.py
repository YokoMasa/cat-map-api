from django.http import HttpResponse, HttpRequest
from django.core.exceptions import ObjectDoesNotExist

from .models import User
from shared import errors

def require_login(f):

  TOKEN_KEY = "HTTP_AUTHORIZATION"

  def decorated(*args, **kwargs):
    if len(args) == 0 or not isinstance(args[0], HttpRequest):
      raise RuntimeError()

    request = args[0]
    if TOKEN_KEY not in request.META:
      print(request.META)
      return HttpResponse(errors.LOGIN_REQUIRED, status=404)

    token = request.META[TOKEN_KEY]
    try:
      user = User.objects.get(token=token)
      return f(request, user, **kwargs)
    except ObjectDoesNotExist:
      return HttpResponse(errors.LOGIN_REQUIRED, status=404)

  return decorated