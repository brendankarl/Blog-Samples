import oci

config = oci.config.from_file()
ai_language_client = oci.ai_language.AIServiceLanguageClient(config)
texttoanalyse = "my details are brendan@brendg.co.uk, I was born in 1981" # String to analyse for PII

batch_detect_language_pii_entities_response = ai_language_client.batch_detect_language_pii_entities( # Identify PII in the string
    batch_detect_language_pii_entities_details=oci.ai_language.models.BatchDetectLanguagePiiEntitiesDetails(
        documents=[
            oci.ai_language.models.TextDocument(
                key="String1",
                text=texttoanalyse,
                language_code="en")],
        compartment_id="Compartment ID"))

cleansedtext = texttoanalyse # Replace the PII in the string with the type of data it is, for example e-mail address
for document in batch_detect_language_pii_entities_response.data.documents:
    for entities in document.entities:
        cleansedtext = cleansedtext.replace((entities.text),("*" + (entities.type) + "*"))

print(cleansedtext)
