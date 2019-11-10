import json

from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import ParseError
from rest_framework import status
from rest_framework.response import Response
from Crypto import Random
from django.conf import settings
from django.core import serializers

from .models.course import Course
from .serializers import CourseSerializer
from .utils.encryptor import Encryptor
from .services.userservice import UserService
from .models.user import User
from .exceptions.benchmarkexception import BenchMarkException
from .authentication import JWTAuthentication
from .utils.commonutils import CommonUtils
from .utils.logger import Logger
from .utils.globalconstants import *



#Initialize Auth Service
userService = UserService()

"""
Method to Register User
"""
@api_view(['POST'])
@permission_classes([AllowAny, ])
@authentication_classes([])
def register_user(request, version):
    try:
        if REQUEST_EMAIL in request.data and REQUEST_PASSWORD in request.data and REQUEST_NAME in request.data:
            name = request.data[REQUEST_NAME]
            email = request.data[REQUEST_EMAIL]
            secret = request.data[REQUEST_PASSWORD]
            user = User(name, email, secret)
            Logger.log("Register User: "+ user.__str__(), INFO)
            user = userService.registerUser(user)
        else:
            return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY: BAD_REQUEST}}, status=status.HTTP_400_BAD_REQUEST)
        
    except BenchMarkException as be:
        Logger.log("BenchMarkException: "+ be.message +": "+ str(be.code) , ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY: be.message}}, status=status.HTTP_409_CONFLICT)
    except (TypeError, ParseError) as te:
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(BAD_REQUEST)}}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        Logger.log("Exception: "+ str(e), ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(e)}},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    response = Response({RESPONSE_KEY:{RESPONSE_DATA_KEY:user}})
    CommonUtils.setJwtInCookie(response, user)
    return response

"""
Method to Authenticate an User
"""
@api_view(['POST'])
@permission_classes([AllowAny, ])
@authentication_classes([])
def authenticate_user(request, version):
    try:
        if REQUEST_EMAIL in request.data and REQUEST_PASSWORD in request.data:
            email = request.data[REQUEST_EMAIL]
            password = request.data[REQUEST_PASSWORD]
            Logger.log("Authenticate User: "+ email, INFO)
            user = userService.authenticate_user(email, password)
        else:
            return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY: BAD_REQUEST}}, status=status.HTTP_400_BAD_REQUEST)
    except BenchMarkException as be:
        Logger.log("BenchMarkException: "+ be.message +": "+ str(be.code) , ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY: be.message}}, status=status.HTTP_401_UNAUTHORIZED)
    except (TypeError, ParseError) as te:
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(BAD_REQUEST)}}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        Logger.log("Exception: "+ str(e), ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    response = Response({RESPONSE_KEY:{RESPONSE_DATA_KEY:user}})
    CommonUtils.setJwtInCookie(response, user)

    return response 


"""
Method to return all Users
"""
@api_view(['GET'])
def users(request, version, user = None):
    try:
        if user is None:
            Logger.log("API Get Users.", INFO)   
        else:
            Logger.log("API Get User: "+ user, INFO)
        data = userService.getUsers(request, user)
    except Exception as e:
        Logger.log("Exception: "+ str(e), ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(e)}}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response({RESPONSE_KEY:{RESPONSE_DATA_KEY:data}})

"""
Method to return all Users
"""
@api_view(['POST'])
def updateUser(request, version):
    try:
        if 'user' in  request.data:
            user = request.data['user']
            Logger.log("API Update User: "+ user['email'], INFO)   
            data = userService.updateUser(user)
        else:
            return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY: BAD_REQUEST}}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        Logger.log("Exception: "+ str(e), ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(e)}}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response({RESPONSE_KEY:{RESPONSE_DATA_KEY:data}})

"""
Method to return all Users
"""
@api_view(['POST'])
def saveFeedback(request, version):
    try:
        if 'feedback' in  request.data:
            feedback = request.data['feedback']
            print(feedback)
            Logger.log("API Save Feedback!", INFO)   
            data = userService.saveFeedback(feedback)
        else:
            return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY: BAD_REQUEST}}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        Logger.log("Exception: "+ str(e), ERROR)
        return Response({RESPONSE_KEY:{ERROR_MESSAGE_KEY:str(e)}}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response({RESPONSE_KEY:{RESPONSE_DATA_KEY:data}})


    


