import boto3

from ..dal.impl.dynamoDbService import DynamoDBService
from ..models.user import User
from ..exceptions.benchmarkexception import BenchMarkException

"""
Data Access layer Class
"""
class DataService:

    """
    Init Method
    """
    def __init__(self):
        self.dynamoDbService = DynamoDBService()

    """
    Call DynamoService create user method
    """
    def saveUser(self, user):
        try:
            self.dynamoDbService.createUser(user)
        except Exception as e:
            raise e
    """
    Call DynamoService get user method
    """
    def getUser(self, user):
        try:
            dbResponse = self.dynamoDbService.getUser(user)
            if dbResponse is None:
                raise BenchMarkException('No User Found!', 901)
            
            return dbResponse
        except Exception as e:
            raise e
    
    """
    Method to get all users
    """
    def getUsers(self, filter):
        try:
            dbResponse = self.dynamoDbService.getUsers(filter)
            return dbResponse
        except Exception as e:
            raise e
    
    """
    Method to update user
    """
    def updateUser(self, user):
        try:
            dbResponse = self.dynamoDbService.updateUser(user)
            return dbResponse
        except Exception as e:
            raise e

    """
    Method to update user feedback
    """
    def saveFeedback(self, feedback):
        try:
            dbResponse = self.dynamoDbService.saveFeedback(feedback)
            return dbResponse
        except Exception as e:
            raise e
    
            
      