import os
from twilio.rest import Client
from datetime import datetime
from zoneinfo import ZoneInfo  # Built-in in Python 3.9+

def lambda_handler(event, context):
    # Twilio credentials
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # Twilio phone number (from where the call will be initiated)
    from_number = "+110987654321"  # Hardcoded Twilio number

    # Support numbers
    india_support_number = "+112345678910"
    us_support_number = "+112345678910"

    # Get the current time in PDT (Pacific Time)
    pdt = ZoneInfo("America/Los_Angeles")
    current_time = datetime.now(pdt)
    ##Example test cases:
    #Monday 8 PM PDT
    #current_time = datetime(2024, 11, 25, 20, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    #Friday 8 PM PDT 
    #current_time = datetime(2024, 11, 22, 20, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    #Sunday 8 PM PDT
    #current_time = datetime(2024, 11, 24, 20, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    #Saturday 10 AM PDT
    #current_time = datetime(2024, 11, 23, 10, 0, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    
    current_day = current_time.weekday()  # Monday=0, Sunday=6
    current_hour = current_time.hour
    

    try:
        # Determine which support number to call based on time and day
        if current_hour == 20:  # 8 PM PDT
            if current_day < 4:  # Monday to Thursday for India support
                to_number = india_support_number
                message = "Calling India Support Team"
            elif current_day == 4:  # Friday, skip the India call
                return {
                    'statusCode': 200,
                    'body': "No call scheduled for India at 8 PM Friday."
                }
            elif current_day == 6:  # Sunday, call India for Monday morning
                to_number = india_support_number
                message = "Calling India Support Team"
            else:
                return {
                    'statusCode': 200,
                    'body': "No call scheduled at this time."
                }
        elif current_hour == 10:  # 10 AM PDT for US support
            if current_day < 5:  # Monday to Friday
                to_number = us_support_number
                message = "Calling US Support Team"
            else:
                return {
                    'statusCode': 200,
                    'body': "No call scheduled for US during weekends."
                }
        else:
            return {
                'statusCode': 200,
                'body': "No call scheduled at this time."
            }

        print(f"Initiating call to {message} at {to_number}")

        # Initiate the call
        call = client.calls.create(
            twiml=f"<Response><Say>{message}</Say></Response>",
            to=to_number,
            from_=from_number
        )

        return {
            'statusCode': 200,
            'body': f"Call initiated to {to_number} with SID: {call.sid}"
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
