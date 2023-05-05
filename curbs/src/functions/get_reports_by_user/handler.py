from aws_lambda_powertools import Logger
from src.functions.get_reports_by_user.index import get_user_reports


logger = Logger(service="get_user_reports")

@logger.inject_lambda_context(log_event=True)
def handler(event, _):
    username = event['requestContext']['authorizer']['jwt']['claims']['sub']
    return get_user_reports(username)
