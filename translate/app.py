import json
import boto3

translate = boto3.client("translate")

def lambda_handler(event, context):
    if "body" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "missing body"
            })
        }

    body = json.loads(event["body"])
    if "text" not in body or type(body["text"]) is not str:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "missing text in body"
            }),
        }
    
    text = body["text"]
    response = translate.translate_text(
        Text=text,
        SourceLanguageCode="en",
        TargetLanguageCode="fr"
    )
    translated_text = response.get("TranslatedText")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": text,
            "translated_text": translated_text,
        }),
    }
