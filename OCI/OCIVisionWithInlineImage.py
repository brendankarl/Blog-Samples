import base64

path = "C:\\Users\\brend\\OneDrive\\Pictures\\Camera Roll\\Photo.jpg" # path to image file
 
def get_base64_encoded_image(image_path): # function that converts image file to Base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image = get_base64_encoded_image(path) # call the function, passing the path of the image

import oci

config = oci.config.from_file() # auth to OCI using the default config file and file

ai_vision_client = oci.ai_vision.AIServiceVisionClient(config) # create the Vision API client

analyze_image = ai_vision_client.analyze_image( #pass the image for analysis to object detection
    analyze_image_details=oci.ai_vision.models.AnalyzeImageDetails(
        features=[
            oci.ai_vision.models.ImageObjectDetectionFeature(
                max_results=130,)],
        image=oci.ai_vision.models.InlineImageDetails(
            source="INLINE",
            data = image),
 compartment_id="Compartment ID")) # update with the OCID of the compartment whose Vision API you'd like to use

analysis = analyze_image.data # put the JSON response returned into a variable

# for each object within the JSON response print it's name and the confidence levels
for object in analysis.image_objects:
    print(str(object.name) + " : " + str(object.confidence))
