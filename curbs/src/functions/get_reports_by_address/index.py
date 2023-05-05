import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger


logger = Logger(service="get_reports_by_address")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CURBS_TABLE_NAME'])

def get_reports_by_address(street_number, street_name, zip_code):
    logger.debug(f"Getting lists for address: {street_number} {street_name} {zip_code}")
    try:
        dynamodb_address = f"{street_number}#{street_name}#{zip_code}"
        response = table.query(
            KeyConditionExpression=Key('PK').eq(dynamodb_address) & Key('SK').begins_with(f"report#")
        )
        reports_for_address = []
        for item in response['Items']:
            report_item = {
                "report_id": item['SK'].replace("report#", "")
            }
            reports_for_address.append(report_item)
        logger.info("response is {}".format(response))
        return {
            "reports": reports_for_address
        }
    except ClientError as err:
        print("An error has occurred")
        print(err)
        raise err