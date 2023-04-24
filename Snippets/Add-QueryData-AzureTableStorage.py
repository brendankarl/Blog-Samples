# pip install azure-data-tables
from azure.data.tables import TableServiceClient
from azure.core.credentials import AzureNamedKeyCredential

accountname = ""
key = ""
endpoint = ""
credential = AzureNamedKeyCredential(accountname,key)

service = TableServiceClient(endpoint=endpoint, credential=credential)
gamestable = service.get_table_client("games")

# add game
entity = {
    'PartitionKey': '1',
    'RowKey': 'Super Mario Land',
    'System': 'GB',
}
gamestable.create_entity(entity)

# Query to return all games
games = gamestable.query_entities(query_filter="PartitionKey eq '1'")
for game in games:
    print(game["RowKey"])

# Query to return games from a specific system
system = "GB"
games = gamestable.query_entities(query_filter="System eq " + "'" + system + "'")
for game in games:
    print(game["RowKey"])
