from utils import client

def collect_s3():
    data = []

    try:
        s3 = client("s3")
        if s3 is None:
            return data

        response = s3.list_buckets()
        for b in response.get("Buckets", []):
            data.append({
                "BucketName": b.get("Name"),
                "CreationDate": b.get("CreationDate")
            })

    except Exception as error:
        print("S3 error:", error)

    return data
