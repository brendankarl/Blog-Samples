import oci

# Read the config created when the API Signing Key was generated
config = oci.config.from_file()

# Create client with the default config file (\.oci\config)
computeclient = oci.core.ComputeClient(config)

# List all of the compute instances within the compartment
list_instances_response = computeclient.list_instances(
    compartment_id="OCID")

# List all of the compute instances
print(list_instances_response.data)
