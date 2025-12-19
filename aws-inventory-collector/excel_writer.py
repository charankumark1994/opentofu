# excel_writer.py
import pandas as pd
from utils import logger

def write_to_excel(dataframes_dict, output_file="aws_inventory.xlsx"):
    try:
        logger.info(f"Writing inventory to {output_file}")

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            for sheet_name, df in dataframes_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        logger.info("Excel report created successfully.")

    except Exception as e:
        logger.error(f"Excel writing error: {e}")
