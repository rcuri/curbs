import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger


logger = Logger(service="get_report_by_id")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CURBS_TABLE_NAME'])


def get_report_by_id(report_id, username):
    logger.debug(f"Getting report: {report_id}")
    dynamodb_report_id = f"REPORT#{report_id}"
    try:
        db_response = table.query(
            KeyConditionExpression=Key('PK').eq(username) & Key('SK').eq(dynamodb_report_id)
        )
        response = {
            "report_id": dynamodb_report_id
        }
        if len(db_response['Items']) > 0:
            response['data'] = db_response['Items'][0]
        else:
            response['data'] = {}
        return response
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err
