# services/s3.py
import pandas as pd
from utils import logger, get_session, remove_tz
from botocore.exceptions import ClientError

def fetch_s3_buckets():
    try:
        session = get_session()
        s3 = session.client("s3")

        logger.info("Collecting S3 buckets...")

        response = s3.list_buckets()
        data = []
        for bucket in response.get("Buckets", []):
            created = bucket["CreationDate"]

            # Fix: convert datetime to string
            created_str = created.strftime("%Y-%m-%d %H:%M:%S")

            data.append({
                "BucketName": bucket["Name"],
                "CreationDate": created_str
        })
        return pd.DataFrame(data)

    except ClientError as e:
        logger.error(f"S3 ClientError: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"S3 Error: {e}")
        return pd.DataFrame()
