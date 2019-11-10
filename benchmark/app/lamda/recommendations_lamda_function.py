import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

"""
Lamda function handler for the Recommendations API
"""
def lambda_handler(event, context):
    
    # Check if user email is present in email
    if 'email' not in event or event['email'] == '' :
        # if not then throw error
        return{
            'statusCode':401,
            'message':'Bad Request'
            }
    
    # Read user email from the header
    email = event['email']
    
    type = None
    if 'type' in event:
        type = event['type']
        
    # Get DynamoDB reference
    dynamodb = boto3.resource('dynamodb')

    # Get Users Table Object
    table = dynamodb.Table('users')

    # Check if user present 
    response = table.get_item(
                Key = {
                    'email':email
                },
                ProjectionExpression = "profile"
                )
    
    # If user is present
    if 'Item' in response:
        user = response['Item']

        # Create payload for Search Lamda function
        payload = {}
        skills = []
        # Recommendations based on Search History
        if type == 'history' and 'searchHistory' in user['profile']:
             user['profile']['searchHistory'].reverse()
             skills = user['profile']['searchHistory']
        elif type == 'interests' and 'interests' in user['profile']:
             user['profile']['interests'].reverse()
             skills = user['profile']['interests']
        else:
             # Read User skills
             user['profile']['skills'].reverse()
             for skillObj in  user['profile']['skills']:
                 skillFilter = {}
                 skillFilter['name'] = skillObj['name']
                 skillFilter['level'] = str(skillObj['level'])
                 skills.append(skillFilter)
                
        if len(skills) > 0:
            payload['skillsArr'] = skills
        else:
            # If no skills are associated to user then set it as None.
            payload['skillsArr'] = None

        # Get lamda client
        lambda_client = boto3.client('lambda')

        # Invoke Lamda Search Function with payload data
        lresponse = lambda_client.invoke(
            FunctionName='search',
            InvocationType='RequestResponse',
            Payload = json.dumps(payload)
            )
        
        # Return Search Response
        return json.loads(lresponse['Payload'].read().decode("utf-8"))
    else:
        # If user is not present, throw error
        return {
            'statusCode': 404,
            'message':"User not found!"
        }
