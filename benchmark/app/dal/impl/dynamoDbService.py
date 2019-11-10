
import boto3
from base64 import b64encode
from boto3.dynamodb.conditions import Key, Attr
from ...exceptions.benchmarkexception import BenchMarkException
from ...models.user import User
from ...utils.globalconstants import *
from ...utils.logger import Logger

"""
Class to call DynamoDB API's
"""
class DynamoDBService:
    
    def __init__(self):
        self.dynamodb = boto3.resource(DYNAMO_DB,aws_access_key_id="AKIA2NBCUYTLCKS4TOXU",aws_secret_access_key="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")
        
    """
    Method to save data to users table
    """ 
    def createUser(self, user):
        try:
            table = self.dynamodb.Table(TABLE_USERS)
            userData = self.getUser(user, table)
            
            if userData is None:
                # Insert User Data to table for new entry
                response = table.put_item(
                Item = vars(user) 
                )
            else:
                # Throw error if user is already registered
                raise BenchMarkException(USER_ALREADY_REGISTERED_MSG, 900)

        except Exception as e:
            raise e
            

    """
    Method to get user using email address
    """
    def getUser(self, user, tableRef = None):
        try:            
            if tableRef is None:
                table = self.dynamodb.Table(TABLE_USERS)
            else:
                table = tableRef
            response = table.get_item(
                Key = {
                    EMAIL_KEY: user.email
                }
                )
            if RESPONSE_ITEM in response:
                return response[RESPONSE_ITEM]

        except Exception as e:
            raise e
        
        return None

    """
    Method to get user using email address
    """
    def getUsers(self, filter):
        try:     
            if 'limit' in filter:
                q_limit = filter['limit']
            else:
                q_limit = 1000
            
            if 'lastIndex' in filter:
                lastIndex = filter['lastIndex']
            else:
                lastIndex = 0

            # values to fetch
            pe = "email, #n, profile"

            # for reserved workds
            ean =  {"#n":"name",}
            table = self.dynamodb.Table(TABLE_USERS)

            if EMAIL_KEY in filter:
                fe = Key(EMAIL_KEY).eq(filter[EMAIL_KEY])
                response = table.scan(
                    FilterExpression = fe,
                    ProjectionExpression = pe,
                    ExpressionAttributeNames = ean,
                    Limit = q_limit,
                )
            else:
                # scan
                response = table.scan(
                    ProjectionExpression = pe,
                    ExpressionAttributeNames = ean,
                    Limit = q_limit,
                )
            
            users = {
                'users': response[RESPONSE_ITEMS],
                'totalCount': table.item_count
            }
            return users
            
        except Exception as e:
            raise e
    
    """
    Method to update user
    """
    def updateUser(self, user):
        try:
            
            table = self.dynamodb.Table(TABLE_USERS)
            userModel = User()
            userModel.email = user[EMAIL_KEY]

            dbUser = self.getUser(userModel, table)

            if dbUser is not None:
                # Update user devices if present in the request    
                if REQUEST_DEVICE in user and user[REQUEST_DEVICE] is not None:
                    devices = []
                    if DEVICES in dbUser[PROFILE] and user[REQUEST_DEVICE] not in dbUser[PROFILE][DEVICES]:
                        dbUser[PROFILE][DEVICES].append(user[REQUEST_DEVICE])
                    elif DEVICES not in dbUser[PROFILE]:
                        devices.append(user[REQUEST_DEVICE])
                        dbUser[PROFILE][DEVICES] = devices

                # Update user search history if present in the request
                if REQUEST_SEARCH_TEXT in user and user[REQUEST_SEARCH_TEXT] is not None:
                    # Logic to handle user search history update
                    searchHistory = []
                    if SEARCH_HISTORY in dbUser[PROFILE] and user[REQUEST_SEARCH_TEXT] not in dbUser[PROFILE][SEARCH_HISTORY]:
                        dbUser[PROFILE][SEARCH_HISTORY].append(user[REQUEST_SEARCH_TEXT])
                    elif SEARCH_HISTORY not in dbUser[PROFILE]:
                        searchHistory.append(user[REQUEST_SEARCH_TEXT])
                        dbUser[PROFILE][SEARCH_HISTORY] = searchHistory

                # Update user skills if present in the request
                if USER_SKILLS in user:
                    dbUser[PROFILE][USER_SKILLS] = user[USER_SKILLS]

                # Update user insterests if present in the request
                if USER_INTERESTS in user:
                    dbUser[PROFILE][USER_INTERESTS] = user[USER_INTERESTS]
                

                # Update user Name if updated
                name = dbUser[USER_NAME]
                if USER_NAME in user:
                    name = user[USER_NAME]

                # Invoke update query
                response = table.update_item(
                Key={
                    EMAIL_KEY: user[EMAIL_KEY]
                },
                # for reserved workds
                UpdateExpression="set profile = :p, #n = :n",
                ExpressionAttributeNames = {"#n":"name",},
                ExpressionAttributeValues = {
                    ':p': dbUser[PROFILE] ,
                    ':n': name
                } 
                )
                return dbUser
            else:
                raise BenchMarkException(USER_NOT_FOUND_MESSAGE, 900)

            return None
        except Exception as e:
            raise e

    """
    Method to save user feedback
    """
    def saveFeedback(self, feedback):
        try:
            table = self.dynamodb.Table(TABLE_FEEDBACK)
            
            if feedback is not None:
                # Insert User Data to table for new entry
                response = table.put_item(
                Item = feedback
                )

                return response
            else:
                # Throw error if user is already registered
                raise BenchMarkException(FEEDBACK_NOT_IN_REQUEST, 900)

        except Exception as e:
            raise e


        
        
        
            
