import boto3
from botocore.config import Config

my_config = Config(
    region_name = "us-west-2",
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)
client = boto3.client(
    'sagemaker-runtime',
    aws_access_key_id="AKIA5VTJBCU57PFFHO3K",
    aws_secret_access_key="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",
    config=my_config
)

endpoint_name = 't5Large'
body = "But both are more interested in a simpler but computationally more challenging puzzle: whether there are more answers for the sum of three cubes for 3. “There are four very easy solutions that were known to the mathematician Louis J. Mordell, who famously wrote in 1953, ‘I do not know anything about the integer solutions of x3 + y3 + z3 = 3 beyond the existence of the four triples (1, 1, 1), (4, 4, -5), (4, -5, 4), (-5, 4, 4); and it must be very difficult indeed to find out anything about any other solutions.’ This quote motivated a lot of the interest in the sum of three cubes problem, and the case k=3 in particular."
print("--------------------------------------------------------------------")
print(body)
print("--------------------------------------------------------------------")
res = client.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=body,
    ContentType='application/json'
)
result = json.loads(res['Body'].read().decode())
