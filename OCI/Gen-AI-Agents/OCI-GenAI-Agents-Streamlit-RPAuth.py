import streamlit as st
import time
import oci
 
# Page Title
st.title("OCI Generative AI Agents Demo 🧠") # Update this with your own title
 
# Sidebar Image
st.sidebar.image("https://brendg.co.uk/wp-content/uploads/2021/05/myavatar.png") # Update this with your own image
 
# OCI GenAI settings

rps = oci.auth.signers.get_resource_principals_signer() # Use Resource Principal for authentication (container instance authenticates to the Gen AI Agent service))
service_ep = "https://agent-runtime.generativeai.us-chicago-1.oci.oraclecloud.com" # Update this with the appropriate endpoint for your region, a list of valid endpoints can be found here - https://docs.oracle.com/en-us/iaas/api/#/en/generative-ai-agents-client/20240531/
agent_ep_id = "ocid1.genaiagentendpoint.oc1.us-chicago-1.amaaaaaaayvpzvaa" # Update this with your own agent endpoint OCID, this can be found within Generative AI Agents > Agents > (Your Agent) > Endpoints > (Your Endpoint) > OCID
 
# Response Generator
def response_generator(textinput):
    # Initialize service client with default config file
    generative_ai_agent_runtime_client = oci.generative_ai_agent_runtime.GenerativeAiAgentRuntimeClient(config={},signer=rps,service_endpoint=service_ep)
 
    # Create Session
    create_session_response = generative_ai_agent_runtime_client.create_session(
        create_session_details=oci.generative_ai_agent_runtime.models.CreateSessionDetails(
            display_name="USER_Session",
            description="User Session"),
        agent_endpoint_id=agent_ep_id)
 
    sess_id = create_session_response.data.id
 
    response = generative_ai_agent_runtime_client.chat(
        agent_endpoint_id=agent_ep_id,
        chat_details=oci.generative_ai_agent_runtime.models.ChatDetails(
            user_message=textinput,
            session_id=sess_id))
 
    #print(str(response.data))
    response = response.data.message.content.text
    return response
 
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
 
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
# Accept user input
if prompt := st.chat_input("How can I help?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
 
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = response_generator(prompt)
        write_response = st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
