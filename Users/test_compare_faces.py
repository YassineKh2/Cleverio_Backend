# import cv2
# import numpy as np
# import os
# import sys

# # Define the path to the media folder
# MEDIA_FOLDER = r"C:\Users\Zeineb Ben Mami\Documents\Django\backold\Cleverio_Backend\Cleverio_Backend\media\profile_pics"

# def load_and_preprocess_image(image_path):
#     # Load the image and convert it to grayscale
#     image = cv2.imread(image_path)
#     if image is None:
#         print(f"Error: Unable to load image {image_path}.")
#         sys.exit(1)
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Use OpenCV's face detector
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    
#     # Check if exactly one face is found
#     if len(faces) != 1:
#         print(f"Error: Expected one face in {image_path}, but found {len(faces)}.")
#         sys.exit(1)
    
#     # Crop to the detected face region
#     (x, y, w, h) = faces[0]
#     face_region = gray_image[y:y+h, x:x+w]
#     return face_region

# def compare_faces(image_path):
#     # Load and preprocess the image twice (for testing self-comparison)
#     face1 = load_and_preprocess_image(image_path)
#     face2 = load_and_preprocess_image(image_path)
    
#     # Initialize the LBPH face recognizer
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
    
#     # Train the recognizer with the first image as "label 1"
#     recognizer.train([face1], np.array([1]))

#     # Predict the label for the second face
#     label, confidence = recognizer.predict(face2)

#     # Display the result based on confidence
#     if confidence < 50:  # Lower confidence means a better match
#         print("The faces are the same.")
#     else:
#         print("The faces are different.")

# if __name__ == "__main__":
#     # Set the image path to `z.jpg` in the media folder
#     image_path = os.path.join(MEDIA_FOLDER, "z.jpg")
    
#     # Run the comparison on itself
#     compare_faces(image_path)
