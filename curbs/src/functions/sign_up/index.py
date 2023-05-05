import boto3
from botocore import exceptions as aws_exceptions
import os
from http import HTTPStatus
import json
from src.services.users import UserService
from aws_lambda_powertools import Logger


logger = Logger(service="sign_up")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CURBS_TABLE_NAME'])

def sign_up_user(first_name, last_name, email, password):
    try:
        user_service = UserService()
        sign_up_response = user_service.sign_up(
            first_name, last_name, email, password
        )
        # User will be identified in table by their Cognito ID
        sign_up_response_json = sign_up_response.json()
        cognito_user_id = sign_up_response_json["cognito_user_id"]
        logger.info("User successfully registered with Cognito service")
        logger.debug("Cognito response is {}".format(sign_up_response))
        db_response = table.put_item(
            Item={
                "PK": cognito_user_id,
                "SK": "USER",
                "first_name": first_name,
                "last_name": last_name
            }
        )
        logger.info("Successfully added user to Curbs table")
        logger.debug("DynamoDB put_item response is {}".format(db_response))
        response = {
            "message": "User successfully signed up"
        }
        return response  
    except Exception as e:
        raise e
        print(e)
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "message": str(e)
        }
