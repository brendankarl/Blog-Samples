import pandas as pd
import oci
import time

# Connect to OCI
config = oci.config.from_file()
nosql_client = oci.nosql.NosqlClient(config)

# Read Excel file
excelfilepath = '/Users/bkgriffi/Downloads/Retro Games Collection.xlsx'
excel = pd.ExcelFile(excelfilepath)
sheets = excel.sheet_names

# Write the data to the Oracle NoSQL Database table
for sheet in sheets:
    print("----------")
    print(sheet)
    print("----------")
    excel = pd.read_excel(excelfilepath,header = None, sheet_name= sheet)
    i = 0
    while i < len(excel[0]) - 1:
        print(excel[0][i])
        update_row_response = nosql_client.update_row(
        table_name_or_id="Games",
        update_row_details=oci.nosql.models.UpdateRowDetails(
        value={'ID': int((str(time.time()).split(".")[0])), 'Game': excel[0][i], 'System': sheet},
        compartment_id="Compartment ID,
        option="IF_ABSENT",
        is_get_return_row=True))
        i += 1
