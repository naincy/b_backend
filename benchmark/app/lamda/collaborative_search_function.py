import json
import itertools
from collections import Counter
import boto3
from boto3.dynamodb.conditions import Key, Attr

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    jaccard_score = float(len(s1.intersection(s2)) / len(s1.union(s2)))
    extra_items = [x for x in s2 if x not in s1]
    if extra_items:
        return {'jaccard_score':jaccard_score,'extra_items':extra_items}
    else:
        return {'jaccard_score':jaccard_score}

def lambda_handler(event, context):

    email = "defaul"
    if 'email' in event:
        email = event['email']
        
    # Get DynamoDB reference
    dynamodb = boto3.resource('dynamodb')

    # Get Users Table Object
    table = dynamodb.Table('users')
    
      # values to fetch
    pe = "profile.searchHistory"
    
    # Getting current user's data
    currentuser_response = table.get_item(
                Key = {
                    'email':email
                },
                ProjectionExpression = pe
                )

    # Filtering required data for current user
    currentuser_search = sorted(list(set([x.lower() for x in currentuser_response['Item']['profile']['searchHistory']])))
    
    # Getting all users' data
    allusers_response = table.scan(
                ProjectionExpression = pe
                )
    
    # Filtering required data for all users
    allusers_search = [sorted(list(set([z.lower() for z in y]))) for y in [x['profile']['searchHistory'] for x in allusers_response['Items']]]
    
    # Getting all possible combinations of search data
    combos = [t for t in itertools.combinations(allusers_search, 2) if len(t[0])!=0 and len(t[1])!=0]
    
    # Getting combinations relevant for current user
    currentuser_combos = [(currentuser_search,t[0]) if t[1]==currentuser_search else t for t in combos] 
    
    # Getting recommendations sorted in the order of Jaccard scores
    sorted_recommendations = sorted([jaccard_similarity(x, y) for x,y in currentuser_combos], key = lambda i: i['jaccard_score'],reverse=True)
    
    # Getting relevant recommendations by verifying if "extra_items" exists
    relevant_recommendations = [item for sublist in [x['extra_items'] for x in sorted_recommendations if 'extra_items' in x and x['jaccard_score']>0.5] for item in sublist]
    
    # Getting top recommendations for the current user
    top_recommendations = [x for x in list(Counter(relevant_recommendations)) if x not in currentuser_search]
    
    # Final response
    return {
        'statusCode': 200,
        'searchHistory': currentuser_search,
        'topSearchRecommendations': top_recommendations
    }
