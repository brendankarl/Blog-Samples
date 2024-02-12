# pip install oci
import oci
import json
import datetime

# Read the config created when the API Signing Key was generated
config = oci.config.from_file()

# Initialize service client with default config file
usage_api_client = oci.usage_api.UsageapiClient(config)

dateto = datetime.date.today().replace(day=1) # Get todays date
month, year = (dateto.month-1, dateto.year) if dateto.month != 1 else (12, dateto.year-1)
datefrom = dateto.replace(day=1, month=month, year=year)

# Build request
request_summarized_usages_response = usage_api_client.request_summarized_usages(
    request_summarized_usages_details=oci.usage_api.models.RequestSummarizedUsagesDetails(
        tenant_id="Tenant OCID",
        time_usage_started=(datefrom.strftime('%Y-%m-%dT%H:%M:%SZ')),
        time_usage_ended=(dateto.strftime('%Y-%m-%dT%H:%M:%SZ')),
        granularity="MONTHLY",
        is_aggregate_by_time=False,
        query_type="COST",
        group_by_tag=[
            oci.usage_api.models.Tag(
                namespace="Oracle-Tags",
                key="CreatedBy")],
        compartment_depth=6))

output = request_summarized_usages_response.data

i = 0
while i < len(output.items):
    print(output.items[i].tags[0].value + " Cost: " + "£" + str(output.items[i].computed_amount))
    i += 1
