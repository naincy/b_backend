import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .utils.logger import Logger
from .utils.globalconstants import *

"""
Custom Authentication Class
"""
class JWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):
        #try:
            #if JWT_KEY not in request.COOKIES:
                #raise AuthenticationFailed('Invalid token.')
            
            #jwtVal = (request.COOKIES[JWT_KEY])[2:-1]
            #decodeValue = jwt.decode(str.encode(jwtVal), settings.SECRET_KEY, algorithm = 'HS256')

        #except Exception as e:
            #Logger.log('Path: {}, Exception: {}'.format(request.META.get('PATH_INFO'),str(e)),ERROR)
            #raise AuthenticationFailed(e)
        
        return (True,None)
        
        