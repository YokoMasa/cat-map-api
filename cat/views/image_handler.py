from datetime import datetime
from io import BytesIO

from PIL import Image

from cat.models import Cat, CatImage

def save_cat_image(cat, user, uploaded_image):
  timestamp_format = "%Y%m%d%H%M%S"
  timestamp = datetime.now().strftime(timestamp_format)
  file_name = timestamp + uploaded_image.name
  thumbnail_file_name = "thumbnail_" + file_name

  cat_image = CatImage(cat=cat, user=user)

  thumbnail_data = _create_thumbnail_data(uploaded_image.file)
  cat_image.raw_image.save(file_name, uploaded_image, False)
  cat_image.thumbnail.save(thumbnail_file_name, thumbnail_data, False)
  cat_image.save()

  cat.catimage_set.add(cat_image)

def _create_thumbnail_data(raw_image_file):
  img = Image.open(raw_image_file)
  img_format = img.format
  exif = img._getexif()
  if exif:
    img = _convert_image(img, exif)
  thumbnail_size = (200, 200)
  img.thumbnail(thumbnail_size)
  thumbnail_data = BytesIO()
  img.save(thumbnail_data, format=img_format)
  return thumbnail_data

def _convert_image(img, exif):
  orientation = exif.get(0x112, 1)
  convert_image = {
    # そのまま
    1: lambda img: img,
    # 左右反転
    2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
    # 180度回転
    3: lambda img: img.transpose(Image.ROTATE_180),
    # 上下反転
    4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
    # 左右反転＆反時計回りに90度回転
    5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90),
    # 反時計回りに270度回転
    6: lambda img: img.transpose(Image.ROTATE_270),
    # 左右反転＆反時計回りに270度回転
    7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270), 
    # 反時計回りに90度回転
    8: lambda img: img.transpose(Image.ROTATE_90),
  }
  if orientation == 0:
    return img
  else:
    return convert_image[orientation](img)