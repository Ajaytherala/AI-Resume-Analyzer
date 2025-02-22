import boto3
import json
import base64
from io import BytesIO
import botocore.config
from pypdf import PdfReader
from requests_toolbelt.multipart import decoder


def fetch_text_content(resume_file):
    resume_bytes = base64.b64decode(resume_file)
    resume_data = PdfReader(BytesIO(resume_bytes))
    resume_content = ""
    for page in resume_data.pages:
        resume_content += page.extract_text()
    return resume_content

def analyze_resume(resume_file:str, job_description:str)->str:
    resume_content = fetch_text_content(resume_file)
    prompt = f"""Given : {job_description} 
    Analyze {resume_content} and output the following information in a JSON (with no additional text)
    "%/ of skills match": "(%/ of skills matched)"
    "Experience level match":"(yes/no)"
    "Skills Mismatched" : "(List of skills mismatched From job description)"
    "Why I would be Ideal Candidate for the role ?" : "(short description With no more than 100 words)"
    """
    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.5,
        "top_p": 0.8,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }
    try:
        bedrock = boto3.client("bedrock-runtime", region_name = "us-west-2",
                               config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
        response = bedrock.invoke_model(body = json.dumps(payload), modelId = "anthropic.claude-3-5-haiku-20241022-v1:0")
        response_content = response["body"].read().decode("utf-8")
        response_data = json.loads(response_content)
        response_analysis = response_data["content"][0]["text"]
        
        return response_analysis
    except Exception as e:
        print("Exception Occurred while analyzing ....",e)
        return ""

def lambda_handler(event, context):
    try:
        body = base64.b64decode(event["body"])
        content_type = event["headers"]["content-type"]
        multipart_data = decoder.MultipartDecoder(body, content_type)
        event_data = {}
        for part in multipart_data.parts:
            content_disposition = part.headers.get(b'Content-Disposition', b'').decode()
            if 'filename' not in content_disposition:
                field_name = content_disposition.split('name="')[1].split('"')[0]
                event_data[field_name] = part.content.decode('utf-8')  
            else:
                event_data["file_content"] = base64.b64encode(part.content).decode('utf-8')

        job_description = event_data["job_description"]
        resume_file = event_data["file_content"]
        resume_analysis = analyze_resume(resume_file, job_description)
        return {
            'statusCode': 200,
            'body': json.dumps(resume_analysis, indent = 4)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({"error":str(e)})
        }