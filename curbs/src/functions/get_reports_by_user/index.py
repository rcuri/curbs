import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger


logger = Logger(service="get_user_reports")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CURBS_TABLE_NAME'])

def get_user_reports(username):
    logger.debug(f"Getting reports for user: {username}")
    try:
        response = table.query(
            KeyConditionExpression=Key('PK').eq(username) & Key('SK').begins_with(f"REPORT#")
        )
        report_items = []
        for item in response['Items']:
            report_item = {
                "report_id": item['SK'].replace("REPORT#", ""),
                "status": item['status'],
                "created_at": item['created_at']
            }
            report_items.append(report_item)
        logger.info("response is {}".format(response))
        return {
            "report_items": report_items
        }
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err