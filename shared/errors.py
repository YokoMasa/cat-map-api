def _error(code):
  return "{error_code: %d}" % code

LOGIN_REQUIRED = _error(1001)
LOGIN_FAILED = _error(1002)
NOT_FOUND = _error(1003)
INSUFFICIENT_PARAMS = _error(1004)