import json
import boto3
import os
import urllib.request

# Get table name from SSM Parameter Store
ssm = boto3.client('ssm')
dynamodb = boto3.resource('dynamodb')

# Function to return the DynamoDB table
def get_table():
    param = ssm.get_parameter(Name='/config/cdk_demo/dynamodb/table_name')
    table_name = param['Parameter']['Value']
    return dynamodb.Table(table_name)

# Function to handle "GET" request
def handle_get(event):
    table = get_table()
    name = event['queryStringParameters'].get('name')
    response = table.get_item(Key={'Name': name})
    item = response.get('Item')
    if item:
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Name not found'})
        }

# Function to handle "POST" request
def handle_post(event):
    table = get_table()
    
    try:
        # Parse request body
        data = event.get("body", "{}")
        name = json.loads(data).get("name", None)

        # Read EKS service endpoint from environment variable
        eks_url = os.environ.get("EKS_MICROSERVICE_URL")
        if not eks_url:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "EKS_MICROSERVICE_URL not configured"})
            }

        # PSend request to service in EKS
        headers = {"Content-Type": "application/json"}
        req = urllib.request.Request(eks_url + "/review", data=data.encode('utf-8'), headers=headers, method='POST')

        # Process the response from the EKS service
        with urllib.request.urlopen(req) as response:
            response_body = response.read().decode('utf-8')
            response_data = json.loads(response_body) 
            item = {
                'Name': name,
                'review': response_data["review"],
            }
            # Write to the DynamoDB table
            db_response = table.put_item(Item = item)            
            return {
                "statusCode": response.getcode(),
                "body": json.dumps(response_data)
            }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Main function
def main(event, context):
    method = event.get('httpMethod')
    
    if method == 'GET':
        return handle_get(event)
    elif method == 'POST':
        return handle_post(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }