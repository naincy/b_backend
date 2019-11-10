import json
import boto3
import types
from boto3.dynamodb.conditions import Key, Attr
from operator import itemgetter

"""
Lamda function handler for search API
"""
def lambda_handler(event, context):
    
    skill = None
    skillsArr = None
    
    recommendationMap = {}
    recommendationMap['1'] = ["Beginner", "Intermediate"]
    recommendationMap['2'] = ["Intermediate", "Advance"]
    recommendationMap['3'] = ["Advance"]
    
    # Search box API
    if 'skills' in event:
        skill = event['skills'].lower()
     
    levels = None  
    if 'levels' in event and event['levels'] != '':
        levels = event['levels'].split(',')
        

    # Depending on user Skills  
    if 'skillsArr' in event:
        skillsArr = event['skillsArr']
    
    # Get Dynamo DB Instance
    dynamodb = boto3.resource('dynamodb')

    # Get Table object
    table = dynamodb.Table('courses')
    results = []
    
    # If user skills are passed
    if skillsArr is not None and len(skillsArr) > 0:
        
        # For each skills
        for item in skillsArr:
            
            if isinstance(item, str):
                fe = (Attr('searchKeys').contains(item.lower()) | Attr('title').contains(item.lower()))
            else:
                fe = (Attr('searchKeys').contains(item['name'].lower()) | Attr('title').contains(item['name'].lower())) & Attr('level').is_in(recommendationMap[item['level']])
                
            # Perform search
            response = table.scan(
                FilterExpression = fe
            )
            # Append results into single array
            results = results + response['Items']
    # If skills search is done   
    elif skill is not None and skill != '':
            
        if levels is not None and len(levels) > 0:
        # if levels are present in request
            response = table.scan(
                    FilterExpression = (Attr('searchKeys').contains(skill) | Attr('title').contains(skill)) & Attr('level').is_in(levels)
                )
        else:
            response = table.scan(
                    FilterExpression = Attr('searchKeys').contains(skill) | Attr('title').contains(skill)
                )
        results = response['Items']
    # Fallback scenario
    else:
        if levels is not None and len(levels) > 0:
        # if levels are present in request
            response = table.scan(
                    FilterExpression = Attr('level').is_in(levels)
                )
        else:
            # To complete table scan
            response = table.scan()
        
        results = response['Items']
    
    results.sort(key=lambda item: item['views'], reverse=True) 
    # return courses for searched skills   
    return {
        'courses': results
    }
