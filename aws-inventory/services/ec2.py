from utils import client

def collect_ec2(region):
    data = []
    try:
        ec2 = client("ec2", region)
        if ec2 is None:
            return data
        resp = ec2.describe_instances()
        for reservation in resp.get("Reservations", []):
            for i in reservation.get("Instances", []):
                data.append({
                    "Region": region,
                    "InstanceId": i.get("InstanceId"),
                    "InstanceType": i.get("InstanceType"),
                    "State": i.get("State", {}).get("Name"),
                    "PrivateIP": i.get("PrivateIpAddress"),
                    "PublicIP": i.get("PublicIpAddress"),
                    "LaunchTime": i.get("LaunchTime")
                })
    except Exception as e:
        print(f"EC2 error in {region}: {e}")
    return data
