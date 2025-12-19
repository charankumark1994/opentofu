import pandas as pd

def save_to_excel(data_dict, filename="AWS_Inventory_collector.xlsx"):
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for service_name, records in data_dict.items():
            df = pd.DataFrame(records)
            # Excel sheet names must be <= 31 chars
            sheet_name = service_name[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print("Excel report generated:", filename)
