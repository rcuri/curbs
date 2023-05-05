import boto3
import os
import uuid
from datetime import datetime

dynamodb = boto3.client('dynamodb')
table_name = os.environ['CURBS_TABLE_NAME']

def submit_report(
        notes, username, curb_type, report_type, proposed_change,
        longitude, latitude, street_number, street_name, zip_code, 
        city, state, country, direction
        ):
    report_uuid = str(uuid.uuid4())
    report_id = f"REPORT#{report_uuid}"
    timestamp = datetime.now().isoformat(timespec='seconds')
    address = f"{street_number}#{street_name}#{zip_code}"
    report_data = {
        "PK": username,
        "SK": report_id,
        "status": "SUBMITTED",
        "created_at": timestamp,
        "address": address,
        "direction": direction,
        "latitude": latitude,
        "longitude": longitude,
        "notes": notes,
        "curb_type": curb_type,
        "report_type": report_type,
        "proposed_change": proposed_change,
        "GSI1PK": report_id,
        "GSI1SK": timestamp
    }
    try:
        db_response = dynamodb.put_item(
            TableName=table_name,            
            Item={
                "PK": {
                    "S": report_data['PK']
                },
                "SK": {
                    "S": report_data['SK']
                },
                "status": {
                    "S": report_data['status']
                },
                "created_at": {
                    "S": report_data['created_at']
                },
                "address": {
                    "S": report_data['address']
                },
                "direction": {
                    "S": report_data['direction']
                },        
                "latitude": {
                    "S": report_data['latitude']
                },
                "longitude": {
                    "S": report_data['longitude']
                },
                "notes": {
                    "S": report_data['notes']
                },
                "curb_type": {
                    "S": report_data['curb_type']
                },
                "report_type": {
                    "S": report_data['report_type']
                },
                "proposed_change": {
                    "S": report_data['proposed_change']
                },
                "GSI1PK": {
                    "S": report_data['GSI1PK']
                },
                "GSI1SK": {
                    "S": report_data['GSI1SK']
                }                
            }
        )
    except Exception as err:
        raise err
    # Create location item
    try:
        location_data = {
            "PK": address,
            "SK": "location",
            "last_report_submitted": timestamp,
            "contains_incorrect_curbs": "Unknown",
            "city": city,
            "state": state,
            "country": country
        }
        location_response = dynamodb.put_item(
            TableName=table_name,
            Item={
                "PK": {
                    "S": location_data['PK']
                },
                "SK": {
                    "S": location_data['SK'] 
                },
                "last_report_submitted": {
                    "S": location_data['last_report_submitted']
                },
                "contains_incorrect_curbs": {
                    "S": location_data['contains_incorrect_curbs']
                },
                "city": {
                    "S": location_data['city'] 
                },
                "state": {
                    "S": location_data['state']
                },
                "country": {
                    "S": location_data['country']
                }
            }
        )
    except Exception as err:
        raise err
    try:
        location_report_data = {
            "PK": address,
            "SK": f"report#{report_id}",
            "created_by": username
        }
        location_report_response = dynamodb.put_item(
            TableName=table_name,
            Item={
                "PK": {
                    "S": location_report_data['PK']
                },
                "SK": {
                    "S": location_report_data['SK'] 
                },
                "created_by": {
                    "S": location_report_data['created_by']
                }
            }
        )
        response = {
            "message": "Successfully submitted report",
            "report_id": report_id
        }
        return response
    except Exception as err:
        raise err    