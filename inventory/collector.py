import pandas as pd
import boto3
from services.ec2 import fetch_ec2_instances
from services.s3 import fetch_s3_buckets
from services.ebs import fetch_unused_volumes
from services.costs import fetch_costs
from excel_writer import write_to_excel
from utils import logger

def get_all_regions():
    try:
        ec2 = boto3.client("ec2")
        response = ec2.describe_regions(AllRegions=False)
        return [r["RegionName"] for r in response["Regions"]]
    except Exception as e:
        logger.error(f"Error fetching regions: {e}")
        return []

def main():
    logger.info("Starting AWS Inventory Collection...")

    regions = get_all_regions()
    logger.info(f"Regions found: {regions}")

    # EC2 Instances
    all_ec2 = []
    for region in regions:
        df = fetch_ec2_instances(region)
        all_ec2.append(df)
    ec2_df = pd.concat(all_ec2, ignore_index=True) if all_ec2 else pd.DataFrame()

    # S3 Buckets
    s3_df = fetch_s3_buckets()

    # Unused EBS Volumes
    all_vols = []
    for region in regions:
        df = fetch_unused_volumes(region)
        all_vols.append(df)
    ebs_df = pd.concat(all_vols, ignore_index=True) if all_vols else pd.DataFrame()

    # Costs
    cost_df = fetch_costs()

    # Write to Excel
    write_to_excel({
        "EC2_Instances": ec2_df,
        "S3_Buckets": s3_df,
        "Unused_EBS": ebs_df,
        "AWS_Costs": cost_df
    })

    logger.info("Inventory collection completed successfully.")

if __name__ == "__main__":
    main()
