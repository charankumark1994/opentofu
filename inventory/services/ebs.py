# services/ebs.py
import boto3
import pandas as pd
from utils import logger

def fetch_unused_volumes(region):
    try:
        logger.info(f"Fetching unused EBS volumes in {region}")
        ec2 = boto3.client("ec2", region_name=region)

        paginator = ec2.get_paginator("describe_volumes")
        page_iterator = paginator.paginate(
            Filters=[{"Name": "status", "Values": ["available"]}]
        )

        volumes = []

        for page in page_iterator:
            for vol in page["Volumes"]:
                volumes.append({
                    "VolumeId": vol["VolumeId"],
                    "Size(GB)": vol["Size"],
                    "VolumeType": vol["VolumeType"],
                    "Region": region,
                    "State": vol["State"],
                    "CreateTime": vol["CreateTime"].strftime("%Y-%m-%d"),
                    "Encrypted": vol.get("Encrypted", False)
                })

        logger.info(f"Found {len(volumes)} unused volumes in {region}")
        return pd.DataFrame(volumes)

    except Exception as e:
        logger.error(f"Error fetching EBS volumes in {region}: {e}")
        return pd.DataFrame()
