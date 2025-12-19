import pandas as pd
from utils import logger, remove_tz

def fetch_lambdas(session, region):
    logger.info(f"Fetching Lambda functions in {region}")
    lambda_client = session.client('lambda', region_name=region)
    data = []
    try:
        response = lambda_client.list_functions()
        for fn in response['Functions']:
            tags = {}
            try:
                tags = lambda_client.list_tags(Resource=fn['FunctionArn']).get('Tags', {})
            except:
                pass
            data.append({
                'FunctionName': fn.get('FunctionName'),
                'Runtime': fn.get('Runtime'),
                'LastModified': remove_tz(fn.get('LastModified')),
                'Tags': tags
            })
        df = pd.DataFrame(data)
        logger.info(f"Found {len(df)} Lambda functions in {region}")
        return df
    except Exception as e:
        logger.error(f"Error fetching Lambda functions: {e}")
        return pd.DataFrame()
