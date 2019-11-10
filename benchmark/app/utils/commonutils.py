import jwt
import datetime

from django.conf import settings
from .globalconstants import *

class CommonUtils:

    @staticmethod
    def create_jwt(payload):
        user = {
            "name": payload["name"],
            "email": payload["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 120)
        }
        
        return jwt.encode(user, settings.SECRET_KEY, algorithm = JWT_ALGO)

    @staticmethod
    def set_cookie(response, key, value, expire=None):
        if expire is None:
            max_age = 24*60*60  #one year
        else:
            max_age = expire
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() +
                                             datetime.timedelta(seconds=max_age), COOKIE_DATE_FORMAT)
        
        response["jwt"] = value
        response.set_cookie(key, value, max_age=max_age,
                            expires=expires,
                            domain=settings.SESSION_COOKIE_DOMAIN,
                            secure=settings.SESSION_COOKIE_SECURE or None)

    
    @staticmethod
    def setJwtInCookie(response, payload):
        jwt = CommonUtils.create_jwt(payload)
        CommonUtils.set_cookie(response, JWT_KEY, jwt)