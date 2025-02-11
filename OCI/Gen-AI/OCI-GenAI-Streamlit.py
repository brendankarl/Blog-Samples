import oci
import streamlit as st

st.set_page_config(page_title="OCI GenAI Demo Front-End",page_icon="🤖")
st.title("OCI GenAI Demo Front-End 🤖")
st.sidebar.image("https://brendg.co.uk/wp-content/uploads/2021/05/myavatar.png")

# GenAI Settings
compartment_id = "Compartment OCID"
config = oci.config.from_file(profile_name="DEFAULT")
endpoint = "https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com"
model_id = "Model OCID"

def chat(question):
    generative_ai_inference_client = oci.generative_ai_inference.GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10,240))
    chat_detail = oci.generative_ai_inference.models.ChatDetails()
    chat_request = oci.generative_ai_inference.models.CohereChatRequest()
    chat_request.message = question 
    chat_request.max_tokens = 1000
    chat_request.temperature = 0
    chat_request.frequency_penalty = 0
    chat_request.top_p = 0.75
    chat_request.top_k = 0
    chat_request.seed = None
    chat_detail.serving_mode = oci.generative_ai_inference.models.OnDemandServingMode(model_id=model_id)
    chat_detail.chat_request = chat_request
    chat_detail.compartment_id = compartment_id
    chat_response = generative_ai_inference_client.chat(chat_detail)
    return chat_response.data.chat_response.text

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What do you need assistance with?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = chat(prompt)
        write_response = st.write(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
