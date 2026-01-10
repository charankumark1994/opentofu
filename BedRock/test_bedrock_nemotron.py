import boto3
import json

# Create Bedrock Runtime client
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Prompt
prompt = "Explain Amazon Bedrock in simple words."

# Request body (NVIDIA Nemotron format)
request_body = {
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "max_tokens": 50,
    "temperature": 0.2
}

try:
    response = bedrock_runtime.invoke_model(
        modelId="nvidia.nemotron-nano-12b-v2",
        body=json.dumps(request_body),
        contentType="application/json"
    )

    # Read and parse response
    response_body = json.loads(response["body"].read())

    print("\nModel Response:\n")
    print(response_body["choices"][0]["message"]["content"])

except Exception as e:
    print("Error invoking model:")
    print(e)
