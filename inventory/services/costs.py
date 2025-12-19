# services/costs.py
import boto3
import pandas as pd
from datetime import datetime, timedelta
from utils import logger

def fetch_costs():
    try:
        logger.info("Fetching AWS costs...")
        ce = boto3.client("ce")
        end = datetime.utcnow().date()
        start = end - timedelta(days=30)

        response = ce.get_cost_and_usage(
            TimePeriod={"Start": str(start), "End": str(end)},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
        )

        costs = []
        for result in response["ResultsByTime"]:
            for group in result["Groups"]:
                costs.append({
                    "Service": group["Keys"][0],
                    "Cost": group["Metrics"]["UnblendedCost"]["Amount"],
                    "Start": result["TimePeriod"]["Start"],
                    "End": result["TimePeriod"]["End"]
                })

        df = pd.DataFrame(costs)
        logger.info("AWS costs fetched successfully.")
        return df

    except Exception as e:
        logger.error(f"Error fetching costs: {e}")
        return pd.DataFrame()
