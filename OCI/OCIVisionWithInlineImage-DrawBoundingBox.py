import base64
import oci
import cv2
import numpy as np

imagepath = "D:\\Pictures\\Camera Roll\\Photo.jpg" # path of the image to analyse
imagewritepath = "D:\\Pictures\Camera Roll\\PhotoBoundingBox.jpg" # image to create with bounding box
 
def get_base64_encoded_image(image_path): # encode image to Base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image = get_base64_encoded_image(imagepath)

config = oci.config.from_file()
ai_vision_client = oci.ai_vision.AIServiceVisionClient(config)

# Detect object
analyze_image = ai_vision_client.analyze_image(
    analyze_image_details=oci.ai_vision.models.AnalyzeImageDetails(
        features=[
            oci.ai_vision.models.ImageObjectDetectionFeature(
                max_results=10,)],
        image=oci.ai_vision.models.InlineImageDetails(
            source="INLINE",
            data = image),
        compartment_id="Compartment ID"))

analysis = analyze_image.data
print("Analysis complete, image contains: " + (analysis.image_objects[0].name))

# Read the image from the location
img = cv2.imread(imagepath)

# Define the polygon vertices using the first object detected in the image
vertices = np.array([((analysis.image_objects[0].bounding_polygon.normalized_vertices[0].x), (analysis.image_objects[0].bounding_polygon.normalized_vertices[0].y)), ((analysis.image_objects[0].bounding_polygon.normalized_vertices[1].x), (analysis.image_objects[0].bounding_polygon.normalized_vertices[1].y)),
                     ((analysis.image_objects[0].bounding_polygon.normalized_vertices[2].x), (analysis.image_objects[0].bounding_polygon.normalized_vertices[2].y)),((analysis.image_objects[0].bounding_polygon.normalized_vertices[3].x), (analysis.image_objects[0].bounding_polygon.normalized_vertices[3].y))])

# Convert the normalized vertices to pixel coordinates
height, width = img.shape[:2]
pixels = np.array([(int(vertex[0] * width), int(vertex[1] * height)) for vertex in vertices])

# Draw the polygon on the image
cv2.polylines(img, [pixels], True, (0, 255, 0), 10)

# Save the updated image
cv2.imwrite(filename=imagewritepath,img=img)
