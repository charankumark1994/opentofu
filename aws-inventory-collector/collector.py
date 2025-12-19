# collector.py
import pandas as pd
import boto3
from services.ec2 import fetch_ec2_instances
from services.s3 import fetch_s3_buckets
from excel_writer import write_to_excel
from utils import logger

def get_all_regions():
    try:
        ec2 = boto3.client("ec2")
        response = ec2.describe_regions(AllRegions=False)
        regions = [r["RegionName"] for r in response["Regions"]]
        return regions
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        return []

def main():
    logger.info("Starting AWS Inventory Collection...")

    regions = get_all_regions()
    logger.info(f"Regions found: {regions}")

    # Collect EC2
    all_ec2 = []
    for region in regions:
        df = fetch_ec2_instances(region)
        all_ec2.append(df)

    ec2_df = pd.concat(all_ec2, ignore_index=True) if all_ec2 else pd.DataFrame()

    # Collect S3
    s3_df = fetch_s3_buckets()

    # Write to Excel
    write_to_excel({
        "EC2_Instances": ec2_df,
        "S3_Buckets": s3_df
    })

    logger.info("Inventory collection completed successfully.")

if __name__ == "__main__":
    main()
