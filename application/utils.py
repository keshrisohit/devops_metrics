import json
def make_response(status_code, body, headers):
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': headers
    }
