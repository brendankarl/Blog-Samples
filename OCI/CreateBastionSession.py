# This script queries the active sessions on a given OCI bastion (bastionocid), if it doesn't find a session for the specified server (serverocid)
# it will create a new bastion session and returns the resultant SSH command to connect to the server and copies to the clipboard, simply paste this into a terminal to connect,
# if their is an active session for the server, it returns the SSH command to connect to the server and copies to the clipboard, simply paste into a terminal to connect

# pip install oci - if you don't have this installed
import oci
# pip install pyperclip - if you don't have this installed
import pyperclip
import json
import time

# OCID of the bastion to query
bastionocid = "BASTIONOCID"
# OCID of the server to connect to
server = "SERVEROCID"
# Private key
privatekeypath = "D:\\OCI\\OCI.key" # Update to the correct location of the private key, this script was developed on Windows, hence the double slashes.
# Public key used for auth to bastion (using the same key for the VM too, to make it simple)
publickey = "PUBLICKEY" # Copy/paste the content of the public key file (.pub)

# Read the config created when the API Signing Key was generated
config = oci.config.from_file()
# Create client with the default config file (\.oci\config)
bastionclient = oci.bastion.BastionClient(config)
# List the current sessions
bastionsessions = bastionclient.list_sessions(bastion_id = bastionocid)
sessionsJSON = json.loads(str((bastionsessions.data)))
# See if there is an active session for the server, if there isn't create one
for session in sessionsJSON:
    if session["lifecycle_state"] == "ACTIVE" and session["target_resource_details"]["target_resource_id"] == server:
        print("Active Session Found : " + session["display_name"])
        # Get the session and return the ssh command generated
        getsession = bastionclient.get_session(session_id = session["id"])
        sshcmd = getsession.data.ssh_metadata["command"]
        # Automate connecting - replace the placeholder for private key with the correct location
        sshcmd = sshcmd.replace("<privateKey>",privatekeypath)
        # Copy the SSH command to the clipboard so that it can be pasted into PowerShell
        pyperclip.copy(sshcmd)
        break
    else:
        print("No active session found - creating a session.....")
        create_session_response = bastionclient.create_session(
        create_session_details=oci.bastion.models.CreateSessionDetails(
        bastion_id=bastionocid,target_resource_details=oci.bastion.models.CreateManagedSshSessionTargetResourceDetails(
            session_type="MANAGED_SSH",target_resource_id=server,target_resource_operating_system_user_name="opc"),
            key_details=oci.bastion.models.PublicKeyDetails(public_key_content=publickey),session_ttl_in_seconds = 10800,
        ))
        # Get the session and return the ssh command generated
        time.sleep(120)
        session = bastionclient.get_session(session_id = create_session_response.data.id)
        sshcmd = session.data.ssh_metadata["command"]
        # Automate connecting - replace the placeholder for private key with the correct location
        sshcmd = sshcmd.replace("<privateKey>",privatekeypath)
        # Copy the SSH command to the clipboard so that it can be pasted into PowerShell
        pyperclip.copy(sshcmd)
        print("Session created, paste the resultant SSH command from the clipboard")
        break
