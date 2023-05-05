from aws_lambda_powertools import Logger
from src.functions.get_reports_by_address.index import get_reports_by_address


logger = Logger(service="get_reports_by_address")

@logger.inject_lambda_context(log_event=True)
def handler(event, _):
    street_number = event['queryStringParameters']['street_number']    
    street_name = event['queryStringParameters']['street_name']    
    zip_code = event['queryStringParameters']['zip_code']            
    return get_reports_by_address(street_number, street_name, zip_code)