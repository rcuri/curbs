import json
from src.functions.submit_report.index import submit_report
from aws_lambda_powertools import Logger


logger = Logger(service="submit_report")

@logger.inject_lambda_context(log_event=True)
def handler(event, _):
    username = event['requestContext']['authorizer']['jwt']['claims']['sub']
    body = json.loads(event['body'])
    notes = body['notes']
    curb_type = body['curb_type']
    report_type = body['report_type']
    proposed_change = body['proposed_change']
    longitude = body['longitude']
    latitude = body['latitude']
    street_number = body['street_number']
    street_name = body['street_name']
    zip_code = body['zip_code']
    city = body['city']
    state = body['state']
    country = body['country']
    direction = body['direction']
    return submit_report(
        notes, username, curb_type, report_type, proposed_change,
        longitude, latitude, street_number, street_name, zip_code, 
        city, state, country, direction        
    )
