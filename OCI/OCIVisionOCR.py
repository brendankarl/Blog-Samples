import oci
import json

# Authenticate to the OCI AI Vision Service
config = oci.config.from_file()
ai_vision_client = oci.ai_vision.AIServiceVisionClient(config)

# Set the type of analysis to OCR
featuretype = "TEXT_DETECTION"

# Analyse the image within object storage
analyze_image_response = ai_vision_client.analyze_image(
    analyze_image_details=oci.ai_vision.models.AnalyzeImageDetails(
        features=[
            oci.ai_vision.models.ImageClassificationFeature(
                feature_type=featuretype,
                max_results=300)],
        image=oci.ai_vision.models.ObjectStorageImageDetails(
            source="OBJECT_STORAGE",
            namespace_name="Replace with Object Storage Namespace",
            bucket_name="Replace with the bucket name",
            object_name="Replace with the name of image to analyse"),
        compartment_id="Replace with Compartment ID"),
   )

# Convert to JSON
json = json.loads(str(analyze_image_response.data))

# Print the lines of text identified (each line of text returned in the response with greater than 5 characters)
lines = []
for analysedlines in json["image_text"]["lines"]:
    if len(analysedlines["text"]) > 5:
        print(analysedlines["text"])
        lines.append(analysedlines["text"])
