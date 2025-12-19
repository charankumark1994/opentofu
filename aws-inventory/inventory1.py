import boto3
from botocore.exceptions import ClientError
from openpyxl import Workbook

# -------------------------------
# 1️ Helper Functions
# -------------------------------
def safe_aws_call(func, *args, **kwargs):
    """
    Calls an AWS API function safely with try/except.
    Returns None on AuthFailure / UnrecognizedClientException / UnauthorizedOperation
    """
    try:
        return func(*args, **kwargs)
    except ClientError as e:
        code = e.response.get("Error", {}).get("Code")
        if code in ["AuthFailure", "UnrecognizedClientException", "UnauthorizedOperation"]:
            return None
        print("AWS ClientError:", e)
        return None
    except Exception as e:
        print("Unexpected error:", e)
        return None

def get_all_regions():
    try:
        ec2 = boto3.client("ec2")
        response = safe_aws_call(ec2.describe_regions)
        if response:
            return [r["RegionName"] for r in response["Regions"]]
    except Exception as e:
        print("Error fetching regions:", e)
    return []

# -------------------------------
# 2️ Resource Fetching Functions
# -------------------------------
def get_ec2_instances(region):
    instances = []
    try:
        ec2 = boto3.client("ec2", region_name=region)
        response = safe_aws_call(ec2.describe_instances)
        if not response:
            return instances

        for res in response.get("Reservations", []):
            for inst in res.get("Instances", []):
                instances.append({
                    "Region": region,
                    "InstanceId": inst.get("InstanceId"),
                    "InstanceType": inst.get("InstanceType"),
                    "State": inst.get("State", {}).get("Name"),
                    "PrivateIP": inst.get("PrivateIpAddress"),
                    "PublicIP": inst.get("PublicIpAddress"),
                    "AZ": inst.get("Placement", {}).get("AvailabilityZone"),
                    "Tags": str(inst.get("Tags")),
                })
    except Exception as e:
        print(f"Error fetching EC2 in {region}:", e)
    return instances

def get_s3_buckets():
    buckets = []
    try:
        s3 = boto3.client("s3")
        response = safe_aws_call(s3.list_buckets)
        if not response:
            return buckets

        for b in response.get("Buckets", []):
            buckets.append({
                "BucketName": b.get("Name"),
                "CreationDate": str(b.get("CreationDate")),
            })
    except Exception as e:
        print("Error fetching S3:", e)
    return buckets

def get_lambda_functions(region):
    functions = []
    try:
        lam = boto3.client("lambda", region_name=region)
        response = safe_aws_call(lambda: lam.list_functions())
        if not response:
            return functions

        for fn in response.get("Functions", []):
            functions.append({
                "Region": region,
                "FunctionName": fn.get("FunctionName"),
                "Runtime": fn.get("Runtime"),
                "Memory": fn.get("MemorySize"),
                "Timeout": fn.get("Timeout"),
                "LastModified": fn.get("LastModified"),
            })
    except Exception as e:
        print(f"Error fetching Lambda in {region}:", e)
    return functions
'''
def get_rds_instances(region):
    rds_instances = []
    try:
        rds = boto3.client("rds", region_name=region)
        response = safe_aws_call(rds.describe_db_instances)
        if not response:
            return rds_instances

        for db in response.get("DBInstances", []):
            rds_instances.append({
                "Region": region,
                "DBInstanceIdentifier": db.get("DBInstanceIdentifier"),
                "Engine": db.get("Engine"),
                "Status": db.get("DBInstanceStatus"),
                "Endpoint": str(db.get("Endpoint")),
                "MultiAZ": db.get("MultiAZ"),
                "InstanceClass": db.get("DBInstanceClass"),
                "Storage": db.get("AllocatedStorage"),
            })
    except Exception as e:
        print(f"Error fetching RDS in {region}:", e)
    return rds_instances
    '''

def get_iam_users():
    users = []
    try:
        iam = boto3.client("iam")
        response = safe_aws_call(iam.list_users)
        if not response:
            return users

        for user in response.get("Users", []):
            users.append({
                "UserName": user.get("UserName"),
                "UserId": user.get("UserId"),
                "Arn": user.get("Arn"),
                "CreateDate": str(user.get("CreateDate")),
            })
    except Exception as e:
        print("Error fetching IAM users:", e)
    return users

# -------------------------------
# 3️ Excel Export
# -------------------------------
def write_to_excel(all_data, filename="aws_inventory2.xlsx"):
    try:
        wb = Workbook()
        for idx, (sheet_name, data) in enumerate(all_data.items()):
            if idx == 0:
                ws = wb.active
                ws.title = sheet_name
            else:
                ws = wb.create_sheet(sheet_name)

            if not data:
                continue

            # Write header
            ws.append(list(data[0].keys()))
            # Write rows
            for row in data:
                ws.append(list(row.values()))

        wb.save(filename)
        print(f"Export completed: {filename}")
    except Exception as e:
        print("Error writing Excel:", e)

# -------------------------------
# 4️ Main Function
# -------------------------------
def main():
    regions = get_all_regions()
    all_ec2, all_lambda, all_rds = [], [], []
    
    # Fetch regional resources
    for region in regions:
        all_ec2.extend(get_ec2_instances(region))
        all_lambda.extend(get_lambda_functions(region))
        all_rds.extend(get_rds_instances(region))

    # Fetch global resources
    s3 = get_s3_buckets()
    iam_users = get_iam_users()

    # Prepare data dictionary
    all_data = {
        "EC2": all_ec2,
        "Lambda": all_lambda,
        #"RDS": all_rds,
        "S3": s3,
        "IAM Users": iam_users,
    }

    # Export to Excel
    write_to_excel(all_data)

if __name__ == "__main__":
    main()
