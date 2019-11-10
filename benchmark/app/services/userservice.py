from ..utils.encryptor import Encryptor
from ..dal.dataservice import DataService
from ..models.user import User
from ..exceptions.benchmarkexception import BenchMarkException
from ..utils.globalconstants import *
from django.conf import settings
import json

"""
User Service Class
"""
class UserService:

    """
    Initialization
    """
    def __init__(self):
        self.dataService =  DataService()

    """
    Method to Register User
    """
    def registerUser(self, userObj):
        try:
            # Encrpyt the password
            cipherText = Encryptor.encrypt(userObj.password)
            userObj.password = cipherText

            # Save user to the Persistance layer
            self.dataService.saveUser(userObj)

            user = {
                 "name": userObj.name,
                 "email": userObj.email,
            }    
        
        except Exception as e:
            raise e
        
        return user

    """
    Method to Authenticate an User
    """
    def authenticate_user(self, email, password):
        user = User()
        try:
            user.email = email

            # Get user data from Data Layer
            user = self.dataService.getUser(user) 

            # Decrypt the password
            decryptedPassword = Encryptor.decrypt(user[REQUEST_PASSWORD].__str__())
            
            # If Password doesnt Match
            if password != decryptedPassword:
                raise BenchMarkException(CREDENTIALS_DOESNT_MATCH, 401)
            
            # Added conditions to show different user experiance post login if skills/interests are not present.
            if len(user[PROFILE][USER_SKILLS]) == 0 and len(user[PROFILE][USER_INTERESTS]) == 0:
                user[IS_USER_DATA_PRESENT] = False
            else:
                user[IS_USER_DATA_PRESENT] = True

            del user[REQUEST_PASSWORD]

        except Exception as e:
            raise e
        
        return user
    
    """
    Method to update user
    """
    def updateUser(self, user):
        try:
            user = self.dataService.updateUser(user) 
            del user[REQUEST_PASSWORD]
            return user
        except Exception as e:
            raise e
 
    """
    Method to get Users
    """
    def getUsers(self, request, user):
        try:
            filter = {} 
            if user is not None:
                filter[REQUEST_EMAIL] = user            
           
            users = self.dataService.getUsers(filter)

            if USER_SKILLS in request.GET:
                searchSkills = json.loads(request.GET.get(USER_SKILLS))
                filteredUser = {'users':[]}
                for user in users['users']:
                    userSkills = user["profile"]["skills"]
                    for filterSkill in searchSkills:
                        for userSkill in userSkills:
                            if filterSkill['name'] == userSkill['name']:
                                filteredUser['users'].append(user)
                                break;

                users = filteredUser;     
            
            return users

        except Exception as e:
            raise e

    """
    Method to save user feedback
    """
    def saveFeedback(self, feedback):
        try:
            response = self.dataService.saveFeedback(feedback)  
            return response
        except Exception as e:
            raise e





