import pyotp
import json
from pydantic import BaseModel
import boto3
import os


class Input(BaseModel):
    secret_key: str
    user_id: str


sns_client = boto3.client("sns")


# document.querySelector("[data-amplify-copy]").querySelector("div").innerHTML
def lambda_handler(event, context):

    input = Input.model_validate_json(event["body"])
    topic_arn = os.environ.get("SNS_TOPIC_ARN")

    otp = pyotp.TOTP(input.secret_key).now()

    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=f"ワンタイムパスワードは{otp}です",
        Subject="OTP",
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
