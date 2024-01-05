import oci
import json

# Read the config
config = oci.config.from_file()

# Create client with the default config file (\.oci\config)
computeclient = oci.core.ComputeClient(config)

# List all of the compute instances within the compartment
list_instances_response = computeclient.list_instances(
    compartment_id="SPECIFY THE COMPARTMENT ID")

# Convert to JSON
instances = json.loads(str(list_instances_response.data))

# Print the state of each VM and stop any that are running
for instance in instances:
 print(instance["display_name"] + " - status: " + instance["lifecycle_state"])
 if instance["lifecycle_state"] == "RUNNING":
   print("Stopping :" + instance["display_name"])
   computeclient.instance_action(instance["id"],"SOFTSTOP")
