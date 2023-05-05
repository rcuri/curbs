from src.functions.get_report_by_id.index import get_report_by_id
from aws_lambda_powertools import Logger


logger = Logger(service="get_report_by_id")

@logger.inject_lambda_context(log_event=True)
def handler(event, _):
    username = event['requestContext']['authorizer']['jwt']['claims']['sub']    
    report_id = event['pathParameters']['report_id']    
    return get_report_by_id(report_id, username)
