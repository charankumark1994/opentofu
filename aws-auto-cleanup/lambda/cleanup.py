import boto3
from datetime import datetime, timezone

ec2 = boto3.resource("ec2")

def lambda_handler(event, context):
    deleted = []

    for instance in ec2.instances.all():
        tags = {t['Key']: t['Value'] for t in instance.tags or []}

        # SAFETY CHECK
        if tags.get("AutoDelete") == "true" and instance.state["Name"] == "stopped":
            print(f"Deleting EC2: {instance.id}")
            instance.terminate()
            deleted.append(instance.id)

    return {
        "status": "success",
        "deleted_ec2_instances": deleted
    }
