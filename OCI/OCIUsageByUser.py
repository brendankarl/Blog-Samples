import oci
import json
import datetime

# Authenticate to OCI
config = oci.config.from_file()

# Initialize the usageapi client service client with the default config file
usage_api_client = oci.usage_api.UsageapiClient(config)

# Create the from and to dates for the usage query - using the previous calendar month
dateto = datetime.date.today().replace(day=1) # Get the first day of the current month
month, year = (dateto.month-1, dateto.year) if dateto.month != 1 else (12, dateto.year-1)
datefrom = dateto.replace(day=1, month=month, year=year) # Get the first day of the previous month

# Build request
request_summarized_usages_response = usage_api_client.request_summarized_usages(
    request_summarized_usages_details=oci.usage_api.models.RequestSummarizedUsagesDetails(
        tenant_id="Tenant OCID", # Update with the tenant OCID
        time_usage_started=(datefrom.strftime('%Y-%m-%dT%H:%M:%SZ')),
        time_usage_ended=(dateto.strftime('%Y-%m-%dT%H:%M:%SZ')),
        granularity="MONTHLY",
        is_aggregate_by_time=False,
        query_type="COST",
        group_by_tag=[
            oci.usage_api.models.Tag( # Return results by the CreatedBy tag, which will indicate the user who created the resource (who the usage cost will be attributed to)
                namespace="Oracle-Tags",
                key="CreatedBy")],
        compartment_depth=6))

# Store the output of the request
output = request_summarized_usages_response.data

# Loop through the output and print the usage cost per user
i = 0
while i < len(output.items):
    print("-" + output.items[i].tags[0].value + " Cost: " + "£" + str(output.items[i].computed_amount))
    i += 1
