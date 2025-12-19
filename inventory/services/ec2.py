# services/ec2.py
import pandas as pd
from utils import logger, get_session #remove_tz
from botocore.exceptions import ClientError

def fetch_ec2_instances(region):
    try:
        session = get_session()
        ec2 = session.client("ec2", region_name=region)

        logger.info(f"Collecting EC2 instances from region: {region}")

        response = ec2.describe_instances()
        data = []

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                launch_time = instance.get("LaunchTime")
                if launch_time:
                    launch_time = launch_time.strftime("%Y-%m-%d %H:%M:%S")
                data.append({
                    "Region": region,
                    "InstanceId": instance.get("InstanceId"),
                    "InstanceType": instance.get("InstanceType"),
                    "State": instance.get("State", {}).get("Name"),
                    "PrivateIP": instance.get("PrivateIpAddress"),
                    "PublicIP": instance.get("PublicIpAddress"),
                    #"LaunchTime": remove_tz(instance.get("LaunchTime"))
                    "LaunchTime": launch_time
                })

        return pd.DataFrame(data)

    except ClientError as e:
        logger.error(f"EC2 ClientError in {region}: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"EC2 Error in {region}: {e}")
        return pd.DataFrame()
