
import json, os, urllib.parse, boto3, logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event))
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')
    size = record['s3']['object'].get('size', 'unknown')

    content_preview = ""
    try:
        if key.lower().endswith(('.txt', '.csv', '.json')) and (size == 'unknown' or int(size) < 5_000_000):
            obj = s3.get_object(Bucket=bucket, Key=key)
            body = obj['Body'].read(500).decode('utf-8', errors='replace')
            content_preview = body
    except Exception as e:
        logger.warning("Could not preview file content: %s", e)

    result = {"bucket": bucket, "key": key, "size": size, "preview": content_preview[:200]}
    logger.info("Processed: %s", json.dumps(result))
    return {"statusCode": 200, "body": json.dumps(result)}
