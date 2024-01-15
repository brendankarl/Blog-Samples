import oci
import base64

# Specify the OCID of the secret to retrieve
keyOCID = "OCID"

# Create vaultsclient using the default config file (\.oci\config) for auth to the API
vaultclient = oci.vault.VaultsClient(config)
config = oci.config.from_file()

# Get the secret
secretclient = oci.secrets.SecretsClient(config)
secretcontents = secretclient.get_secret_bundle(secret_id=keyOCID)

# Decode the secret from base64 and print
keybase64 = secretcontents.data.secret_bundle_content.content
keybase64bytes = keybase64.encode("ascii")
keybytes = base64.b64decode(keybase64bytes)
key = keybytes.decode("ascii")
print(key)
