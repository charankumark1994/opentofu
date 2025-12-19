from utils import get_regions
from excel_writer import save_to_excel

from services.ec2 import collect_ec2
from services.s3 import collect_s3


def main():
    regions = get_regions()
    if not regions:
        print("Could not discover regions.")
        return

    report = {}
    all_ec2 = []

    for region in regions:
        print("Collecting EC2 from:", region)
        all_ec2.extend(collect_ec2(region))

    print("Collecting S3 buckets")
    all_s3 = collect_s3()

    report["EC2"] = all_ec2
    report["S3"] = all_s3

    save_to_excel(report)


if __name__ == "__main__":
    main()
