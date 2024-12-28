import json
import random
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
# DynamoDB table name
TABLE_NAME = 'PositiveAffirmations'

def lambda_handler(event, context):
    # Parse the category from the request, use general as default
    category = event['queryStringParameters'].get('category', 'general')

    # As API was built with Lambda proxy integration, the lambda functions must configure the header:
    headers = {
        "Access-Control-Allow-Origin": "https://posaffirm.s3.eu-west-2.amazonaws.com",
        "Access-Control-Allow-Methods": "GET", 
        "Access-Control-Allow-Headers": "*",  
    }
  
    try:
        # Access the DynamoDB table
        table = dynamodb.Table(TABLE_NAME)

        # Query the DynamoDB table for the given category
        response = table.get_item(Key={'Category': category})

        # If no category is found, use "general" affirmations
        if 'Item' not in response:
            response = table.get_item(Key={'Category': 'general'})

        affirmations = response['Item']['Affirmations']        
        affirmation = random.choice(affirmations)        
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'affirmation': affirmation})
        }
    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            'headers': headers,
            "body": "Failed to load data"
        }
