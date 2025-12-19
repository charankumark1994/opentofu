import boto3

def get_regions():
    try:
        ec2 = boto3.client("ec2")
        resp = ec2.describe_regions(AllRegions=True)
        return [r["RegionName"] for r in resp.get("Regions", [])]
    except Exception as e:
        print("Error discovering regions:", e)
        return []

def client(service, region=None):
    try:
        return boto3.client(service, region_name=region)
    except Exception as e:
        print(f"Error creating client {service} {region}: {e}")
        return None
