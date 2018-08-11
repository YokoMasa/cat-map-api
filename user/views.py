import json
import secrets
import os
from datetime import datetime
from io import BytesIO

import twitter
from requests_oauthlib import OAuth2Session
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError

from shared import errors
from .models import User
from .forms import TwitterLoginForm, GoogleLoginForm

@require_http_methods(["POST"])
def twitter_login(request):
  form = TwitterLoginForm(request.POST)
  if form.is_valid():
    user = _get_twitter_login_user(
      key=form.cleaned_data["access_token_key"],
      secret=form.cleaned_data["access_token_secret"]
    )
    if user:
      return HttpResponse(_get_token_json(user))
    else:
      return HttpResponse(errors.LOGIN_FAILED, status=404)
  else:
    return HttpResponse(errors.LOGIN_FAILED, status=400)

@require_http_methods(["POST"])
def google_login(request):
  form = GoogleLoginForm(request.POST)
  if form.is_valid():
    user = _get_google_login_user(form.cleaned_data["auth_code"])
    if user:
      return HttpResponse(_get_token_json(user))
    else:
      return HttpResponse(errors.LOGIN_FAILED, status=404)
  else:
    return HttpResponse(errors.LOGIN_FAILED, status=400)

def _get_twitter_login_user(key, secret):
  api = twitter.Api(
    consumer_key=os.environ["TW_API_KEY"],
    consumer_secret=os.environ["TW_API_SECRET"],
    access_token_key=key,
    access_token_secret=secret
  )
  tw_user = api.VerifyCredentials()
  if tw_user:
    id = tw_user.id_str
    name = tw_user.name
    user = _find_or_create_sns_login_user(id, name, User.TWITTER)
    return user
  else:
    return None

def _get_google_login_user(auth_code):
  TOKEN_URL = "https://www.googleapis.com/oauth2/v4/token"
  PROFILE_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
  client_id = os.environ["GOOGLE_CLIENT_ID"]
  client_secret = os.environ["GOOGLE_CLIENT_SECRET"]

  oauth = OAuth2Session(client_id)
  oauth.fetch_token(
    TOKEN_URL,
    code=auth_code,
    client_secret=client_secret
  )
  user_data = oauth.get(PROFILE_URL).json()
  if user_data:
    sns_id = user_data["id"]
    sns_name = user_data["name"]
    return _find_or_create_sns_login_user(sns_id, sns_name, User.GOOGLE)
  else:
    return None

def _find_or_create_sns_login_user(sns_user_id, name, login_type):
  try:
    user = User.objects.get(sns_user_id=sns_user_id, login_type=login_type)
    return user
  except ObjectDoesNotExist:
    user = User.objects.create(
      name=name,
      sns_user_id=sns_user_id,
      login_type=login_type,
      token=secrets.token_hex()
    )
    return user

def _get_token_json(user):
  data = {"token": user.token}
  return json.dumps(data, ensure_ascii=False)
